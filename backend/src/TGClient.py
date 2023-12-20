import asyncio
import os
from os import getenv
from typing import Coroutine

from telethon import TelegramClient


class TGClient:
    def __init__(self, config):
        self._MAX_MESSAGES = 29
        if config["dev?"]:
            api_id = os.getenv("dev-app-id")
            api_hash = os.getenv("dev-app-hash")
        else:
            api_id = os.getenv("prod-app-id")
            api_hash = os.getenv("prod-app-hash")

        api_id = int(api_id)

        self._app = TelegramClient("Senahiya", api_id, api_hash)
        self._message_queue = []

    async def _start(self):
        coro = self._app.start()
        await coro

    def start(self):
        asyncio.create_task(self._start())
        asyncio.create_task(self._queue_runner())

    def stop(self):
        self._app.disconnect()

    async def _queue_runner(self):
        loop = asyncio.get_running_loop()

        while loop.is_running():
            if len(self._message_queue) >= self._MAX_MESSAGES:
                tasks_len = self._MAX_MESSAGES
            else:
                tasks_len = len(self._message_queue)

            tasks = []
            for x in range(tasks_len):
                tasks.append(self._message_queue.pop(0))
            await asyncio.gather(*tasks)

            # while self._no_network and loop.is_running():
            #     async with AsyncClient() as client:
            #         try:
            #             await client.get("https://www.google.com/")
            #         except telegram.error.BadRequest as e:
            #             logger.error(e, exc_info=True)
            #             continue
            #         except RequestError:
            #             self._no_network = True
            #         else:
            #             self._no_network = False
            #
            #     await asyncio.sleep(10)

            await asyncio.sleep(1.1)

    async def __send_message(self, receiver: str, message: str):
        await self._app.send_message("", "")

    async def send_message(self):
        await self.__send_message("", "")
