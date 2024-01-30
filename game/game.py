from config import config

class Game(object):
    def __init__(self, target: str) -> None:
        self.retries = config['max_retries']
        self.target = target