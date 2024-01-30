import uvicorn
from wordle import Wordle
from config import config

if __name__ == '__main__':
    wordle = Wordle()
    uvicorn.run(wordle.app, host=config['ip'], port=config['port'])
