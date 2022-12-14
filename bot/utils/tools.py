import asyncio
import time

from typing import Tuple, List, Union, Dict
from .cache import Cache
from pyrogram import types, enums, filters
from bot import bot


def getButtons(
    data: dict, row: int = 3, close: bool = False, back: bool = False
) -> List[List[types.InlineKeyboardButton]]:
    main = []
    sub = []
    for i in data:
        sub.append(types.InlineKeyboardButton(f"{data[i]}", callback_data=i))
        if len(sub) == row:
            main.append(sub.copy())
            sub.clear()
    if len(sub) > 0:
        main.append(sub.copy())
        sub.clear()
    _closeBack = []
    if back:
        _closeBack.append(types.InlineKeyboardButton("🔙 Back", callback_data="back"))
    if close:
        _closeBack.append(types.InlineKeyboardButton("✖️ Close", callback_data="close"))
    if _closeBack:
        main.append(_closeBack)
    return main


def getYesOrNo(yes: str = "✅ Yes", no: str = "✖️ No"):
    return [
        [
            types.InlineKeyboardButton(yes, callback_data="yes"),
            types.InlineKeyboardButton(no, callback_data="no"),
        ]
    ]


async def getCallBackQuery(
    msg: types.Message, silent: bool = False, adminOnly: bool = False
) -> Union[types.CallbackQuery, None]:
    while bot.is_idling:
        try:
            query = await bot.wait_for_callback_query(msg.chat.id, msg.id, timeout=300)
        except asyncio.TimeoutError:
            if silent:
                await msg.delete()
                return None
            await msg.edit("`Maximum time exceeded`", reply_markup=types.ReplyKeyboardRemove())  # type: ignore
            return None
        else:
            if adminOnly:
                _, admins = await getAdmins(msg.chat.id)
                if query.from_user.id not in admins:
                    await query.answer("Unauthorized \n!admin only command")
                    continue
            return query


async def get_input(
    msg: types.Message, timeout: int = 600, silent: bool = False, fromUser: int = None  # type: ignore
):
    while bot.is_idling:
        try:
            text = await bot.wait_for_message(
                msg.chat.id, timeout=timeout, filters=filters.incoming
            )
        except asyncio.TimeoutError:
            if silent:
                await msg.delete()
                return ""
            try:
                await msg.reply(
                    "`Maximum time exceeded.`", reply_markup=types.ReplyKeyboardRemove()
                )
            except Exception:
                pass
            return ""
        else:
            if fromUser and not text.from_user:
                continue
            elif fromUser and fromUser != text.from_user.id:
                continue
            if text.text:
                if text.text.lower() == "/cancel":
                    await msg.reply("`Cancelled`", reply_markup=types.ReplyKeyboardRemove())
                    return ""
                return text.text
            else:
                await msg.reply("`Send as text message.\nUse /cancel to cancel this.`")
                continue


async def getAdmins(
    group: int, force: bool = False
) -> Tuple[Dict[int, types.ChatMember], List[int]]:
    if group in Cache.ADMINS:
        if time.time() - Cache.ADMINS[group]["time"] > 1200:  # type: ignore
            force = True
        if not force:
            return Cache.ADMINS[group]["admins"], Cache.ADMINS[group]["list"]  # type: ignore

    admins = {}
    _list = []
    async for admin in bot.get_chat_members(
        group, filter=enums.ChatMembersFilter.ADMINISTRATORS
    ):  # type: ignore
        admins[admin.user.id] = admin
        _list.append(admin.user.id)
    Cache.ADMINS[group] = {"admins": admins, "list": _list, "time": time.time()}
    return admins, _list

