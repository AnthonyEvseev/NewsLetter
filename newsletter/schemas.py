from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class NewsLetter(BaseModel):
    id: Optional[int] = None
    text: str
    date_start: datetime
    date_stop: datetime
    code: str
    tags: str
