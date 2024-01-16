from fastapi import FastAPI
import asyncio
from app.websockets import run_websocket
from app.consumer import consume

app = FastAPI()


@app.on_event("startup")
async def startup_event():
    kafka_task = asyncio.create_task(consume())
    ws_task = asyncio.create_task(run_websocket())


@app.get("/")
async def read_root():
    return {"message": "Hello World"}


@app.get("/ws/upd")
async def upd():
    global assets
    assets = []
