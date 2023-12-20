import json
from contextlib import asynccontextmanager
from fastapi import FastAPI
from sqlalchemy import Sequence

from src.TGClient import TGClient
from dotenv import load_dotenv

from src.crud.database import engine, getdb
from src.crud.models import *

load_dotenv()
with open("config/config.json", 'r') as file:
    config = json.load(file)

client = TGClient(config)


@asynccontextmanager
async def lifespan(app: FastAPI):
    client.start()

    async with getdb() as db:
        await db.run_sync(Base.metadata.create_all)

    yield
    client.stop()
