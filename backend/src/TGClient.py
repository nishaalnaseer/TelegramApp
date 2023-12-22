import asyncio
import logging
import os
import time
from collections import OrderedDict

from sqlalchemy import select
from telethon.events.newmessage import NewMessage
from telethon import TelegramClient, events

from src.crud.database import async_session
from src.crud.models import OTP, Message, User
from src.crud.utils import insert_object, get_user_by_id, update_user
import telethon.tl.functions.channels as channels

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
        self._ME = None
        api_id = int(api_id)

        _app = TelegramClient("Senahiya", api_id, api_hash)
        self._app = _app
        self._message_queue = []
        self._my_messages = OrderedDict()

        @_app.on(events.NewMessage(pattern='', incoming=True))
        async def _on_message_in(event: NewMessage.Event):
            await self._message_in(event)

        @_app.on(events.NewMessage(pattern='', outgoing=True))
        async def _on_message_out(event: NewMessage.Event):
            await self._message_out(event)

    async def _start(self):
        coro = self._app.start()
        await coro

    async def download(self, channel, limit):
        channel = await self._app.get_entity(channel)
        async for message in self._app.iter_messages(channel, limit=None):
            # Check if the message has media
            if message.media:
                # Download media to the current working directory

                if message.id < limit:
                    break

                await self._app.download_media(
                    message.media,
                    file=f"downloads/{message.id}",
                )
                print(f"Downloaded media from message ID {message.id}")

    async def get_chats(self):
        chats_in = await self._app.get_dialogs(limit=None)
        chats_out = {chat.id: chat.name for chat in chats_in}

        return chats_out

    def start(self):
        asyncio.create_task(self._start())
        asyncio.create_task(self._queue_runner())

    def stop(self):
        self._app.disconnect()

    async def _queue_runner(self):
        loop = asyncio.get_running_loop()

        while not self._app.is_connected():
            logger.info("Not yet connected to telegram, going to sleep")
            await asyncio.sleep(1)

        logger.info("Connected to telegram finishing initialisation "
                    "and starting message queue")
        _me = await self._app.get_me()
        self._ME = _me

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

    async def send_message(self, receiver: str, message: str):
        self._send_message(receiver, message)
        otp = OTP(message=message, receiver=receiver)
        await insert_object(otp)

    async def _message_in(self, event: NewMessage.Event):
        chat_id = event.chat_id
        sender_id = event.sender_id

        sender = await event.get_sender()
        if chat_id != sender_id or sender.bot :
                # or sender_id == self._ME.id: todo correct
            return

        user = User(
            id=sender_id,
            username=sender.username,
            first_name=sender.first_name,
            last_name=sender.last_name,
            phone=sender.phone,
        )

        record = await get_user_by_id(sender_id)
        if record is None:
            await insert_object(user)
        else:
            await update_user(user)

        message = Message(
            id=event.message.id,
            sender=sender_id,
            receiver=self._ME.id,
            message=event.message.message,
            time_sent=event.message.date
        )
        await insert_object(message)

    async def _message_out(self, event: NewMessage.Event):
        # todo remove bot, channel, group input
        message = Message(
            id=event.message.id,
            sender=self._ME.id,
            receiver=event.chat_id,
            message=event.message.message,
            time_sent=event.message.date
        )
        await insert_object(message)

    # async def get_chat_messages(self, limit, user_id):

