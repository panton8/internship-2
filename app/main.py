from fastapi import FastAPI
import asyncio
from app.websockets import run_websocket
from app.consumer import consume
from app.config import Config

app = FastAPI()


@app.on_event("startup")
async def startup_event():
    ws_task = asyncio.create_task(run_websocket())
    kafka_task = asyncio.create_task(consume())


@app.get("/")
async def read_root():
    return {"message": "Hello World"}