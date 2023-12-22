import os
from fastapi import FastAPI, HTTPException
from starlette.requests import Request
from starlette.responses import JSONResponse

from src.crud.utils import select_chat_messages
from src.utils import lifespan, client

app = FastAPI(lifespan=lifespan)
# TODO implement web sockets

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


@app.get("/my/chats")
async def get_chats(request: Request) -> JSONResponse:
    chats = await client.get_chats()

    return JSONResponse(
        content=chats
    )


@app.get("/channel/medias")
async def download_channel_medias(
        channel: int, limit: int
) -> JSONResponse:
    await client.download(channel, limit=limit)
    return JSONResponse(content={"details": "ok"})


@app.get("/messages/chat")
async def get_chat_messages(user: int, limit: int) -> JSONResponse:
    l = await select_chat_messages(user, limit=limit)

    print(l)
