import os
from fastapi import FastAPI, HTTPException
from src.utils import lifespan, client


app = FastAPI(lifespan=lifespan)
us = os.getenv("user-id")
us_password = os.getenv("user-pass")


@app.post("/message/contact")
async def send_message_contact(
        user: str, password: str, text: str, to: str
):

    # i know there can be better auth but rn im too lazy
    if user.lower() != us or \
            password.lower() != us_password:
        raise HTTPException(
            401,
            "Incorrect credentials"
        )

    client.send_message(to, text)
    return {"details": "success"}
