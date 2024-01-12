from pydantic import BaseModel
from datetime import datetime


class Crypto(BaseModel):
    code: str
    exchange_rate: float
    datetime: datetime
