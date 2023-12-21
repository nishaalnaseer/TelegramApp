import asyncio
import json
from contextlib import asynccontextmanager
from fastapi import FastAPI
from sqlalchemy import Sequence
from src.TGClient import TGClient
from dotenv import load_dotenv
from src.crud.utils import initialise_db

load_dotenv()
with open("config/config.json", 'r') as file:
    config = json.load(file)

client = TGClient(config)


@asynccontextmanager
async def lifespan(app: FastAPI):
    asyncio.create_task(initialise_db())
    client.start()

    yield
    client.stop()
