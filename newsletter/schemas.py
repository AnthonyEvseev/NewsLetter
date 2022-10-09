from datetime import date
from typing import Optional
from pydantic import BaseModel


class NewsLetter(BaseModel):
    # id: Optional[int] = None
    text: str
    date_start: date
    date_stop: date
    code: str
    tags: str
