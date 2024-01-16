import ast
from aiokafka import AIOKafkaConsumer
import os
from app.config import Config


async def consume():
    consumer = AIOKafkaConsumer("crypto_list", bootstrap_servers="kafka:9092", group_id="crypto_list")
    await consumer.start()
    try:
        async for msg in consumer:
            if msg is None:
                continue
            data = msg.value.decode('utf-8')
            Config.assets = ast.literal_eval(data)
            print(f">>{Config.assets}")
    finally:
        await consumer.stop()
    print("Consumer stopped")
