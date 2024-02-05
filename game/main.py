import uvicorn
from wordle import Wordle
from config import _config

def main():
    wordle = Wordle(_config)
    uvicorn.run(wordle.app, host=_config.ip, port=_config.port)

if __name__ == '__main__':
    main()
