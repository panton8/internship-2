from app.schemas.crypto import Crypto
from app.db.config import database
import uuid


class CryptoRepo:
    @staticmethod
    async def insert(crypto: Crypto):
        id = str(uuid.uuid4())
        _crypto = {
            "_id": id,
            "code": crypto.code,
            "exchange_rate": crypto.exchange_rate,
            "datetime": crypto.datetime
        }
        await database.get_collection('crypto').insert_one(_crypto)