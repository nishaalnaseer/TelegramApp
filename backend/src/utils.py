import json
from contextlib import asynccontextmanager
from fastapi import FastAPI
from src.TGClient import TGClient
from dotenv import load_dotenv


load_dotenv()
with open("config/config.json", 'r') as file:
    config = json.load(file)

client = TGClient(config)


@asynccontextmanager
async def lifespan(app: FastAPI):
    client.start()
    yield
    client.stop()
