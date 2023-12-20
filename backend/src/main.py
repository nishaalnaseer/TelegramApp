import json
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
# from src.client import TGClient
with open("config/config.json", 'r') as file:
    config = json.load(file)

# client = TGClient(config)
import src.client

app = FastAPI()


@app.post("/jsp/receiveSMS.jsp", status_code=201)
async def otp(user_id: str, password: str, text: str, to: str):
    """
    endpoint to send an otp to telegram account
    :param to: telegram number
    :param user_id: user id in dhiraagu api
    :param password: password in dhiraagu api
    :param text: text
    :return:
    """
    # ?userid=senahiya&password=50923492&to=7365880&text=test

    if user_id.lower() != "senahiya" \
            or password.lower() != "50923492":
        raise HTTPException(
            403,
            "Incorrect Credentials"
        )

    # await client.contact_to_message(contact=to, message=text)

    return {"details": "success"}
