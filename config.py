import os

import motor.motor_asyncio

MONGOBD_URL = os.getenv('MONGO_URL')

client = motor.motor_asyncio.AsyncIOMotorClient(MONGOBD_URL)

database = client.fastAPiDB