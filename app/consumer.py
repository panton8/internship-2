import ast
from aiokafka import AIOKafkaConsumer
from app.config import Config


async def consume():
    consumer = AIOKafkaConsumer(
        bootstrap_servers="kafka:9092",
        group_id="crypto_list"
    )
    await consumer.start()
    consumer.subscribe(["crypto_list"])

    try:
        async for msg in consumer:
            data = msg.value.decode('utf-8')
            Config.assets = ast.literal_eval(data)
    finally:
        await consumer.stop()
