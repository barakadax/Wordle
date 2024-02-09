from pydantic import BaseModel

class config(BaseModel):
    ttl: int
    max_games: int
    max_retries: int
    ip: str
    port: int
    words_path: str 

_config = config(ttl=600,
                 max_games=100,
                 max_retries=5,
                 ip='127.0.0.1',
                 port=8000,
                 words_path='../valid-wordle-words.txt')
