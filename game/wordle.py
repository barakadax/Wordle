import uuid
import random
import unicodedata
from game import Game
from config import config
from cachetools import TTLCache
from fastapi import FastAPI, Body
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException

class Wordle:
    def __init__(self):
        self.app = FastAPI(
            title='Local Wordle',
            description='wordle',
            summary='wordle',
            docs_url=None,
            redocs_url=None,
            version='0.0.1',
            contact={
                'name': 'Barak Taya',
                'url': 'https://www.linkedin.com/in/barakadax/'
            },
            license_info={
                'name': 'AGPL-3.0 license',
                'url': 'https://www.gnu.org/licenses/agpl-3.0.en.html#license-text',
            }
        )

        with open('../valid-wordle-words.txt', 'r') as file:
            self.__words = file.read().split()

        self.__cache = TTLCache(maxsize=config['max_games'], ttl=config['ttl'])

        self.app.exception_handler(HTTPException)(self.__http_exception_handler)
        self.app.get('/')(self.__root)
        self.app.get('/start')(self.__start)
        self.app.get('/play/session/{session}')(self.__play)

    async def __start(self):
        new_session = str(uuid.uuid4())
        word = random.choice(self.__words)
        self.__cache[new_session] = Game(word)
        print(word)

        response = JSONResponse(content={'session': new_session})
        response.status_code = 200
        return response
    
    def __game_logic(self, game: Game, user_input: str) -> JSONResponse:
        if game.retries == 0:
            response = JSONResponse(content={'response': f'Game is finish, word was: {game.target}'})
            response.headers['statues'] = 'done'
            response.status_code = 200
            game.has_won = False
        else:
            game.retries -= 1

            if user_input == game.target:
                response = JSONResponse(content={'response': f'You win!!! the word was: {game.target}'})
                response.headers['statues'] = 'won'
                response.status_code = 200
                game.has_won = True
            else:
                result = { 'retries left': game.retries }
                common_letters = list(set(user_input) & set(game.target))
                for i in range(0, 5):
                    if user_input[i] == game.target[i]:
                        result[i] = 'correct'
                    elif user_input[i] in common_letters:
                        result[i] = 'correct letter wrong placement'
                    else:
                        result[i] = 'wrong'
                response = JSONResponse(content=result)
                response.status_code = 200

        return response

    
    async def __play(self, session: str, data: str = Body(...)):
        if len(data) != 5:
            response = JSONResponse(content={'response': 'Input must be 5 letters long'})
            response.status_code = 200
            return response
        
        user_input = unicodedata.normalize('NFKD', data).casefold()
        if user_input not in self.__words:
            response = JSONResponse(content={'response': 'Not an acceptable word'})
            response.status_code = 200
            return response

        if session in self.__cache:
            game = self.__cache[session]
            if game.has_won is None:
                response = self.__game_logic(game, user_input)
            else:
                response = JSONResponse(content={'response': f'Game already finished the word was "{game.target}" and you have {"won" if game.has_won else "lost"}'})
                response.status_code = 200
        else:
            response = JSONResponse(content={'response': 'this session doesn\'t exists'})
            response.headers['statues'] = 'deleted'
            response.status_code = 404

        return response

    async def __root(self):
        response = JSONResponse(content={'roles': 'Each guess must be a valid 5-letter word\n \
                                         You will get back JSON with for each letter if placement is correct or not and if correct if in the right placement or not'})
        response.status_code = 200
        return response
    
    async def __http_exception_handler(self, request, exc):
        return JSONResponse(status_code=404, content={'detail': 'None existing endpoint'})
