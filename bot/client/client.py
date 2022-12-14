import asyncio
import functools
import logging, os, math
import logging.config
from typing import Dict, Optional, Union
import logging, os, math
from pyrogram import Client, __version__
from pyrogram.raw.all import layer
from pyrogram import Client as PyroClient
from pyrogram import errors, raw, session, types
from pyrogram.filters import Filter
from datetime import datetime
from pytz import timezone
from gutils import temp
from ..config import Config
from ..utils.logger import LOGGER
from pyrogram.errors import BadRequest, Unauthorized
TIMEZONE = (os.environ.get("TIMEZONE", "Asia/Yangon"))
log = LOGGER(__name__)


#LOG_STR += f"Your current IMDB template is {Config.TEMPLATE}"


class ListenerCanceled(Exception):
    pass


class PatchedClient(PyroClient):
    def __init__(
        self,
        name: str,
        bot_token: str = Config.BOT_TOKEN,  # type: ignore
        api_id: int = Config.API_ID,
        api_hash: str = Config.API_HASH,  # type: ignore
        plugins: dict = {"root": "bot/plugins"},
        **kwargs,
    ):
        self.name = name
        self.listeners: Dict[str, Dict[str, Union[asyncio.Future, Filter, None]]] = {}
        super().__init__(
            self.name,
            api_id=api_id,
            api_hash=api_hash,
            bot_token=bot_token,
            plugins=plugins,
            **kwargs,
        )

    async def start(self):
        await super().start()
        
        me = await self.get_me()
        temp.ME = me.id
        temp.U_NAME = me.username
        temp.B_NAME = me.first_name
        temp.B_LINK = me.mention
        self.username = '@' + me.username
        curr = datetime.now(timezone(TIMEZONE))
        date = curr.strftime('%d %B, %Y')
        time = curr.strftime('%I:%M:%S %p')
        #log.info(f"----- {self.me.first_name} [{self.me.id}] started ----\n🌐 Tɪᴍᴇᴢᴏɴᴇ : <code>{TIMEZONE}</code>\n\n🉐 Vᴇʀsɪᴏɴ : <code>v{__version__} (Layer {layer})</code></b>")
        log.info
        if Config.LOG_CHANNEL:
            try:
                await self.send_message(Config.LOG_CHANNEL, text=f"<b> Iꜱ Rᴇsᴛᴀʀᴛᴇᴅ !!\n\n{self.me.first_name} Bot \n\n[{self.me.id}] \n\n📅 Dᴀᴛᴇ : <code>{date}</code>\n⏰ Tɪᴍᴇ : <code>{time}</code>\n🌐 Tɪᴍᴇᴢᴏɴᴇ : <code>{TIMEZONE}</code>\n🉐 Vᴇʀsɪᴏɴ : <code>v{__version__} (Layer {layer})</code></b>")                      
            except Unauthorized:
                LOGGER(__name__).info(f"Bot isn't able to send message to LOG_CHANNEL")
            except BadRequest as e:
                LOGGER.error(e)    

    async def stop(self, *args):
        await super().stop()
        LOGGER(__name__).info(f"----- {self.me.first_name} [{self.me.id}] stopped ---")
        
    """Custom methods for conversation support from pyromod && pyropatch"""

    async def check_cbd(self, buttons: types.InlineKeyboardMarkup):
        if not buttons:
            return False
        for button_row in buttons.inline_keyboard:
            for button in button_row:
                if button.callback_data:
                    return True
        return False

    async def wait_for_callback_query(
        self,
        chat_id: Optional[int] = None,
        message_id: Optional[int] = None,
        inline_message_id: Optional[str] = None,
        timeout: Optional[int] = None,
        filters: Optional[Filter] = None,
    ) -> types.CallbackQuery:
        if chat_id:
            if not message_id:
                raise TypeError("message_id is required")
            msg = await self.get_messages(chat_id, message_id)
            if not msg:
                raise ValueError("message id is invalid")
            if not msg.from_user.is_self:  # type: ignore
                raise ValueError("cannot use self message")
            if not await self.check_cbd(msg.reply_markup):  # type: ignore
                raise TypeError("message type invalid [no callback button]")
            key = f"{chat_id}:{message_id}"
        elif inline_message_id:
            key = inline_message_id
        else:
            raise TypeError("chat_id or inline_message_id is required")
        future = self.loop.create_future()
        future.add_done_callback(functools.partial(self.remove_listener, key))
        self.listeners.update({key: {"future": future, "filters": filters}})
        return await asyncio.wait_for(future, timeout)

    async def wait_for_message(
        self,
        chat_id: Union[str, int],
        filters: Optional[Filter] = None,
        timeout: Optional[int] = None,
    ) -> types.Message:
        if not isinstance(chat_id, int):
            chat = await self.get_chat(chat_id)
            chat_id = chat.id  # type: ignore
        future = self.loop.create_future()
        future.add_done_callback(functools.partial(self.remove_listener, str(chat_id)))
        self.listeners.update({str(chat_id): {"future": future, "filters": filters}})
        return await asyncio.wait_for(future, timeout)

    async def wait_for_inline_query(
        self, user_id: int, filters: Optional[Filter] = None, timeout: Optional[int] = None
    ):
        future = self.loop.create_future()
        future.add_done_callback(functools.partial(self.remove_listener, str(user_id)))
        self.listeners.update({str(user_id): {"future": future, "filters": filters}})
        return await asyncio.wait_for(future, timeout)

    async def wait_for_inline_result(
        self, user_id: int, filters: Optional[Filter] = None, timeout: Optional[int] = None
    ):
        future = self.loop.create_future()
        future.add_done_callback(functools.partial(self.remove_listener, str(user_id)))
        self.listeners.update({str(user_id): {"future": future, "filters": filters}})
        return await asyncio.wait_for(future, timeout)
    

    def remove_listener(self, key: str, future=None):
        if key in self.listeners and future == self.listeners[key]["future"]:
            self.listeners.pop(key)

    def cancel_listener(self, key: str):

        listener = self.listeners.get(key)
        if not listener or listener["future"].done():  # type: ignore
            return
        listener["future"].set_exception(ListenerCanceled())  # type: ignore
        self.remove_listener(key, listener["future"])

    async def invoke(
        self,
        query: raw.core.TLObject,
        retries: int = session.Session.MAX_RETRIES,
        timeout: float = session.Session.WAIT_TIMEOUT,
        sleep_threshold: float = None,  # type: ignore
    ):
        while True:
            try:
                return await super().invoke(
                    query=query,
                    retries=retries,
                    timeout=timeout,
                    sleep_threshold=sleep_threshold,
                )
            except (errors.FloodWait) as e:
                LOGGER(__name__).warning(f"{self.me.first_name} Sleeping for - {e.value} | {e}")
                await asyncio.sleep(e.value + 2)  # type: ignore
            except (TimeoutError, OSError):
                LOGGER(__name__).warning(f"timeout for {self.me.first_name}")
