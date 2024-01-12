import json
from datetime import datetime, timedelta
from fastapi import FastAPI
import websockets
import asyncio
from app.schemas.crypto import Crypto
from app.crud.crud_crypto import CryptoRepo


app = FastAPI()

assets = ['BTCUSDT', 'ETHUSDT', 'LTCUSDT']


async def run_websocket():
    global assets
    while True:
        res = '/'.join([coin.lower() + '@kline_1s' for coin in assets])
        cop = assets
        socket = 'wss://stream.binance.com:9443/stream?streams=' + res
        print("start", res)
        if assets:
            async with websockets.connect(socket) as websocket:
                while True:
                    data = await websocket.recv()
                    parsed_data = json.loads(data)
                    crypto_code = parsed_data['data']['s'][:-4]
                    crypto_rate = parsed_data['data']['k']['c']
                    crypto_time = datetime.fromtimestamp(parsed_data['data']['k']['t'] / 1000) + timedelta(hours=3)
                    crypto_instance = Crypto(code=crypto_code, exchange_rate=crypto_rate, datetime=crypto_time)

                    await CryptoRepo.insert(crypto_instance)
                    if cop != assets:
                        break


@app.on_event("startup")
async def startup_event():
    ws_task = asyncio.create_task(run_websocket())


@app.get("/")
async def read_root():
    return {"message": "Hello World"}


@app.get("/ws/upd")
async def upd():
    global assets
    assets = []
