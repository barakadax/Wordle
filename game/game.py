from typing import Optional
from pydantic import BaseModel

class Game(BaseModel):
    retries: int
    target: str
    has_won: Optional[bool]
