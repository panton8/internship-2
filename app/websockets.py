import json
from datetime import datetime, timedelta
import websockets
from aiokafka import AIOKafkaProducer

from app.schemas.crypto import Crypto
from app.crud.crud_crypto import CryptoRepo
from app.config import Config


async def run_websocket():
    while True:
        res = '/'.join([coin.lower() + '@kline_1s' for coin in Config.assets])
        cop = Config.assets
        socket = 'wss://stream.binance.com:9443/stream?streams=' + res
        if Config.assets:
            async with websockets.connect(socket) as websocket:
                while True:
                    crypto_data = {}
                    for i in range(len(Config.assets)):
                        data = await websocket.recv()
                        parsed_data = json.loads(data)
                        crypto_code = parsed_data['data']['s'][:-4]
                        crypto_rate = parsed_data['data']['k']['c']
                        crypto_time = datetime.fromtimestamp(parsed_data['data']['k']['t'] / 1000) + timedelta(hours=3)
                        crypto_instance = Crypto(code=crypto_code, exchange_rate=crypto_rate, datetime=crypto_time)
                        await CryptoRepo.insert(crypto_instance)
                        crypto_instance.datetime = crypto_instance.datetime.strftime("%Y-%m-%dT%H:%M:%S.%f")
                        crypto_data[crypto_instance.code] = crypto_instance.exchange_rate
                    res_cr = json.dumps(crypto_data).encode('utf-8')
                    producer = AIOKafkaProducer(bootstrap_servers='kafka:9092')
                    await producer.start()
                    try:
                        await producer.send_and_wait('crypto_data', value=res_cr)
                    finally:
                        await producer.stop()
                    if cop != Config.assets:
                        break
