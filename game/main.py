import uvicorn
from wordle import Wordle

if __name__ == '__main__':
    wordle = Wordle()
    uvicorn.run(wordle.app, host='127.0.0.1', port=8000)
