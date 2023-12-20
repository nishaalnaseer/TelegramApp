import asyncio
from os import getenv
import logging
# from telethon import TelegramClient
from dotenv import
logger = logging.getLogger("TGClientlog")


class TGClient:
    def __init__(self, config):
        if config["dev?"]:
            load_env
