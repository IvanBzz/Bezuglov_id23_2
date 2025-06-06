from celery.backends import redis
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from celery.result import AsyncResult
from tasks import crack_rar
import asyncio
import json
import aioredis

app = FastAPI()

# Менеджер WebSocket-соединений
class ConnectionManager:
    def __init__(self):
        self.active_connections = {}
        self.redis = None

    async def connect(self, websocket: WebSocket, task_id: str):
        await websocket.accept()
        self.active_connections[task_id] = websocket

    def disconnect(self, task_id: str):
        if task_id in self.active_connections:
            del self.active_connections[task_id]

    async def send_message(self, message: dict, task_id: str):
        if task_id in self.active_connections:
            websocket = self.active_connections[task_id]
            await websocket.send_json(message)

manager = ConnectionManager()
'''
# Подключение к Redis при старте
@app.on_event("startup")
async def startup_event():
    redis = aioredis.from_url("rediss://localhost:6379", encoding="utf-8", decode_responses=True)
    await redis.ping()
    print("Redis подключён")
    # Присваиваем redis вашему менеджеру
    manager.redis = redis 
'''


# Прослушивание событий из Redis
async def listen_redis():
    pubsub = manager.redis.pubsub()
    await pubsub.subscribe("task_updates")
    async for message in pubsub.listen():
        if message["type"] == "message":
            data = json.loads(message["data"])
            task_id = data["task_id"]
            await manager.send_message(data, task_id)
            if data["status"] in ["success", "failure", "error"]:
                manager.disconnect(task_id)

# WebSocket endpoint
@app.websocket("/ws/{task_id}")
async def websocket_endpoint(websocket: WebSocket, task_id: str):
    await manager.connect(websocket, task_id)
    try:
        while True:
            await websocket.receive_text()  # Поддержание соединения
    except WebSocketDisconnect:
        manager.disconnect(task_id)

# REST endpoint для запуска задачи
@app.post("/crack/")
async def start_crack(file_path: str):
    task = crack_rar.delay(file_path)
    return {"task_id": task.id, "status_url": f"/ws/{task.id}"}