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
    def __init__(self, config: config) -> None:
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

        self.__config = config

        with open('../valid-wordle-words.txt', 'r') as file:
            self.__words = file.read().split()

        self.__cache = TTLCache(maxsize=self.__config.max_games, ttl=self.__config.ttl)

        self.app.exception_handler(HTTPException)(self.__http_exception_handler)
        self.app.get('/')(self.__root)
        self.app.get('/start')(self.__start)
        self.app.get('/play/session/{session}')(self.__play)

    async def __start(self) -> JSONResponse:
        new_session = str(uuid.uuid4())
        word = random.choice(self.__words)
        print(word)
        self.__cache[new_session] = Game(retries=self.__config.max_retries, target=word, has_won=None)

        return JSONResponse(status_code=200, content={'session': new_session})
    
    def __game_logic(self, game: Game, user_input: str) -> JSONResponse:
        if game.retries == 0:
            game.has_won = False

            return JSONResponse(status_code=200,
                                content={'response': f'Game is finished, word was: {game.target}'},
                                headers={'statues': 'done'})
        
        game.retries -= 1

        if user_input == game.target:
            game.has_won = True

            return JSONResponse(status_code=200,
                                content={'response': f'You win!!! the word was: {game.target}'},
                                headers={'statues': 'won'})
        
        result = { 'retries left': game.retries }
        common_letters = list(set(user_input) & set(game.target))
        for counter, (input_char, target_char) in enumerate(zip(user_input, game.target)):
            if input_char == target_char:
                result[counter] = 'correct'
            elif input_char in common_letters:
                result[counter] = 'correct letter wrong placement'
            else:
                result[counter] = 'wrong'

        return JSONResponse(status_code=200, content=result)
    
    async def __play(self, session: str, data: str = Body(...)) -> JSONResponse:
        if len(data) != 5:
            return JSONResponse(status_code=400, content={'response': 'Input must be 5 letters long'})
        
        user_input = unicodedata.normalize('NFKD', data).casefold()
        if user_input not in self.__words:
            return JSONResponse(status_code=403, content={'response': 'Not an acceptable word'})

        if session in self.__cache:
            game = self.__cache[session]
            if game.has_won is None:
                return self.__game_logic(game, user_input)
            return JSONResponse(status_code=208,
                                content={'response': f'Game already finished the word was: {game.target} and you have {"won" if game.has_won else "lost"}'})
        return JSONResponse(status_code=404,
                                    content={'response': 'this session doesn\'t exists'},
                                    headers={'statues': 'deleted'})

    async def __root(self) -> JSONResponse:
        return JSONResponse(status_code=200,
                                content={'roles': 'Each guess must be a valid 5-letter word, \
                                         You will get a JSON back containing: A status for each letter, indicating whether the placement is correct or not.'})
    
    async def __http_exception_handler(self, request, exc):
        return JSONResponse(status_code=404, content={'detail': 'None existing endpoint'})
