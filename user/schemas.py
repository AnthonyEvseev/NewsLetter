from typing import Optional

from pydantic import BaseModel, validator
from enum import Enum


class OperatorTags(str, Enum):
    Beeline = 'beeline'
    MTS = 'mts'
    Megafon = 'megafon'
    Tele2 = 'tele2'


class UserIDSchemas(BaseModel):
    id: Optional[int] = None


class UserSchemas(UserIDSchemas):
    phone_number: str
    tags: OperatorTags
    time_zone: str

    class Config:
        orm_mode = True

    @validator('phone_number')
    def check_phone_number(cls, v):
        if v[0:2] != '79' or len(v) != 11:
            raise ValueError('Вы ввели неверно номер телефона или он не является российским')
        return v
