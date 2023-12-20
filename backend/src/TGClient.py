import asyncio
import json
import logging
import os
from os import getenv
from typing import Coroutine
from telethon.events.newmessage import EventCommon, NewMessage
from telethon import TelegramClient, events

logger = logging.getLogger("TG-Client")


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

        _app = TelegramClient("Senahiya", api_id, api_hash)
        self._app = _app
        self._message_queue = []

        @_app.on(events.NewMessage(pattern=''))
        async def on_message(event: NewMessage.Event):
            chat_id = event.chat_id
            sender_id = event.sender_id

            if chat_id != sender_id:
                self.send_message(
                    chat_id,
                    message="Group messaging not allowed"
                )
                return
            if event.bot:
                self.send_message(
                    chat_id,
                    message="Bots not allowed"
                )
                return

            sender = await event.get_sender()
            print(sender.to_json())

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
        try:
            await self._app.send_message(receiver, message)
        except Exception as e:
            logger.error(e, exc_info=True)

    def _send_message(self, receiver, message, **kwargs):
        coro = self.__send_message(receiver, message)
        self._message_queue.append(coro)

    def send_message(self, receiver, message):
        self._send_message(receiver, message)

