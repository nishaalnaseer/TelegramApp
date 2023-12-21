import os
from fastapi import FastAPI, HTTPException
from starlette.requests import Request

from src.utils import lifespan, client


app = FastAPI(lifespan=lifespan)


def validate_client(_client: str):
    return _client == "127.0.0.1" or \
        _client[:8] == "10.62.12" or _client[:8] == "10.62.10"


@app.post("/message/contact")
async def send_message_contact(
        request: Request, text: str, to: str
):
    _client = request.client.host

    if not validate_client(client):
        raise HTTPException(
            status_code=403,
            detail="Forbidden to users"
        )

    await client.send_message(to, text)
    return {"details": "success"}
