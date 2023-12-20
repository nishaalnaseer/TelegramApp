from fastapi import FastAPI
from src.utils import lifespan, client

app = FastAPI(lifespan=lifespan)


@app.post("/message/contact")
async def send_message_contact():
    await client.send_message()
    return {"details": "success"}
