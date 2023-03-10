#!/usr/bin/env python3
# Copyright (C) @ZauteKm
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

from __future__ import unicode_literals

import asyncio
import math
import os
import time
import requests 
import os

import aiofiles
import aiohttp
import wget
from pyrogram import Client, filters
from pyrogram.errors import FloodWait, MessageNotModified
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message 
from youtubesearchpython import SearchVideos
from yt_dlp import YoutubeDL
import youtube_dl
from youtube_search import YoutubeSearch



API = "https://apis.xditya.me/lyrics?song="


# Convert hh:mm:ss to seconds
def time_to_seconds(time):
    stringt = str(time)
    return sum(int(x) * 60 ** i for i, x in enumerate(reversed(stringt.split(':'))))

@Client.on_message(filters.command(["song", "music", "mp3"]) & ~filters.channel & ~filters.edited)
def a(client, message: Message):
    urlissed = get_text(message)
    query = ''
    reply_id = message.reply_to_message.message_id if message.reply_to_message else message.message_id
    for i in message.command[1:]:
        query += ' ' + str(i)
    print(query)
    m = message.reply(f"**๐๐ แแพแฌแแฑแธแแฑแแซแแแบ โบ๏ธ .. \nแแฎแแฎแแปแแบแธแแญแฏ ๐ ** `{urlissed}`", reply_to_message_id=reply_id)
    ydl_opts = {"format": "bestaudio[ext=m4a]"}
    try:
        results = []
        count = 0
        while len(results) == 0 and count < 6:
            if count>0:
                time.sleep(1)
            results = YoutubeSearch(query, max_results=1).to_dict()
            count += 1
        # results = YoutubeSearch(query, max_results=1).to_dict()
        try:
            link = f"https://youtube.com{results[0]['url_suffix']}"
            # print(results)
            title = results[0]["title"]
            thumbnail = results[0]["thumbnails"][0]
            duration = results[0]["duration"]
            views = results[0]["views"]

            ## UNCOMMENT THIS IF YOU WANT A LIMIT ON DURATION. CHANGE 1800 TO YOUR OWN PREFFERED DURATION AND EDIT THE MESSAGE (30 minutes cap) LIMIT IN SECONDS
            # if time_to_seconds(duration) >= 1800:  # duration limit
            #     m.edit("Exceeded 30mins cap")
            #     return

            performer = f"[แแญแฏแแญแฏแแบแแฑแธ ๐]" 
            thumb_name = f'thumb{message.message_id}.jpg'
            thumb = requests.get(thumbnail, allow_redirects=True)
            open(thumb_name, 'wb').write(thumb.content)

        except Exception as e:
            print(e)
            m.edit('**แแฎแแปแแบแธแแฌแแแบแแซ แแแฑแธโแแฒแแฒแท แแฑแซแแบแธแแฑแซแแบแแญแฏแแบแกแฏแถแธแแแบ ๐!\n* แแฑแซแแบแธแแฑแซแแบแแแฌแแฒ แแแบแแฝแฑแแฌแแฑแแผแฎแธ ๐ </a>\nMusic แแพแฌแแแบแธ\n /song music name \n{ แฅแแแฌ - /song แแฑแแแญแฏแแฒ } *')
            return
    except Exception as e:
        m.edit(
            "**โฆ๏ธ Music แแพแฌแแแบแธ /song music name { แฅแแแฌ - /song แแฑแแแญแฏแแฒ } `"
        )
        print(str(e))
        return
    m.edit(
       "`๐  แแพแฌแแฝแฑแแฌ แแแบแแฑแธแแฑแแซแแแบ \nแแแแฑแฌแแทแบแแซแแฑแฌแบ ๐๐... Upload......โฃ๏ธ`",    
    )
    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(link, download=False)
            audio_file = ydl.prepare_filename(info_dict)
            ydl.process_info(info_dict)
        rep = f'๐ต <b> ๐ป๐๐๐๐:</b> <a href="{link}">{title}</a>\n<b>๐  แแฑแฌแแบแธแแญแฏแแฐ  : <i><b>{message.from_user.mention}</b>\n<b>๐  แแพแฌแแฑแธแแฐ       : <i><b>{message.chat.title}</b>\n๐ค Uploaded By : <a href="https://t.me/Painglay15">ยฉ  Ko Paing </a><b>\n<b><a href="https://t.me/mksviplink">ยฉ MKS Channel</a></b>' 
        secmul, dur, dur_arr = 1, 0, duration.split(':')
        for i in range(len(dur_arr)-1, -1, -1):
            dur += (int(dur_arr[i]) * secmul)
            secmul *= 60
        message.reply_audio(audio_file, caption=rep, parse_mode='HTML',reply_to_message_id=reply_id, title=title, duration=dur, performer=performer, thumb=thumb_name)
        m.delete()
        message.delete()
    except Exception as e:
        m.edit('**แแฌแแพแแบแธแแแญแแฒแท Error แแฑแธแแแบแแฝแฌแธแแซแแแบ ๐ฅฒ แแผแแบแแพแฌแแผแแทแบแแซแแฑแฌแบ \n\n@PAINGLAY15 !!**')
        print(e)
    try:
        os.remove(audio_file)
        os.remove(thumb_name)
    except Exception as e:
        print(e)


def get_text(message: Message) -> [None, str]:
    text_to_return = message.text
    if message.text is None:
        return None
    if " " not in text_to_return:
        return None
    try:
        return message.text.split(None, 1)[1]
    except IndexError:
        return None


def humanbytes(size):
    if not size:
        return ""
    power = 2 ** 10
    raised_to_pow = 0
    dict_power_n = {0: "", 1: "Ki", 2: "Mi", 3: "Gi", 4: "Ti"}
    while size > power:
        size /= power
        raised_to_pow += 1
    return str(round(size, 2)) + " " + dict_power_n[raised_to_pow] + "B"


async def progress(current, total, message, start, type_of_ps, file_name=None):
    now = time.time()
    diff = now - start
    if round(diff % 10.00) == 0 or current == total:
        percentage = current * 100 / total
        speed = current / diff
        elapsed_time = round(diff) * 1000
        if elapsed_time == 0:
            return
        time_to_completion = round((total - current) / speed) * 1000
        estimated_total_time = elapsed_time + time_to_completion
        progress_str = "{0}{1} {2}%\n".format(
            "".join("โฃ๏ธ" for i in range(math.floor(percentage / 10))),
            "".join("๐ง" for i in range(10 - math.floor(percentage / 10))),
            round(percentage, 2),
        )

        tmp = progress_str + "{0} of {1}\nETA: {2}".format(
            humanbytes(current), humanbytes(total), time_formatter(estimated_total_time)
        )
        if file_name:
            try:
                await message.edit(
                    "{}\n**File Name:** `{}`\n{}".format(type_of_ps, file_name, tmp)
                )
            except FloodWait as e:
                await asyncio.sleep(e.x)
            except MessageNotModified:
                pass
        else:
            try:
                await message.edit("{}\n{}".format(type_of_ps, tmp))
            except FloodWait as e:
                await asyncio.sleep(e.x)
            except MessageNotModified:
                pass


def get_user(message: Message, text: str) -> [int, str, None]:
    asplit = None if text is None else text.split(" ", 1)
    user_s = None
    reason_ = None
    if message.reply_to_message:
        user_s = message.reply_to_message.from_user.id
        reason_ = text or None
    elif asplit is None:
        return None, None
    elif len(asplit[0]) > 0:
        user_s = int(asplit[0]) if asplit[0].isdigit() else asplit[0]
        if len(asplit) == 2:
            reason_ = asplit[1]
    return user_s, reason_


def get_readable_time(seconds: int) -> int:
    count = 0
    ping_time = ""
    time_list = []
    time_suffix_list = ["s", "m", "h", "days"]
    while count < 4:
        count += 1
        remainder, result = divmod(seconds, 60) if count < 3 else divmod(seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)
    for x in range(len(time_list)):
        time_list[x] = str(time_list[x]) + time_suffix_list[x]
    if len(time_list) == 4:
        ping_time += time_list.pop() + ", "
    time_list.reverse()
    ping_time += ":".join(time_list)
    return ping_time


def time_formatter(milliseconds: int) -> str:
    seconds, milliseconds = divmod(int(milliseconds), 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    tmp = (
        ((str(days) + " day(s), ") if days else "")
        + ((str(hours) + " hour(s), ") if hours else "")
        + ((str(minutes) + " minute(s), ") if minutes else "")
        + ((str(seconds) + " second(s), ") if seconds else "")
        + ((str(milliseconds) + " millisecond(s), ") if milliseconds else "")
    )
    return tmp[:-2]


def get_file_extension_from_url(url):
    url_path = urlparse(url).path
    basename = os.path.basename(url_path)
    return basename.split(".")[-1]


# Funtion To Download Song
async def download_song(url):
    song_name = f"{randint(6969, 6999)}.mp3"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                f = await aiofiles.open(song_name, mode="wb")
                await f.write(await resp.read())
                await f.close()
    return song_name


is_downloading = False


def time_to_seconds(time):
    stringt = str(time)
    return sum(int(x) * 60 ** i for i, x in enumerate(reversed(stringt.split(":"))))


@Client.on_message(filters.command(["vsong", "video", "mp4"]))
async def vsong(client, message: Message):
    urlissed = get_text(message)
    reply_id = message.reply_to_message.message_id if message.reply_to_message else message.message_id

    pablo = await client.send_message(
        message.chat.id, f"**๐๐ แแพแฌแแฑแธแแฑแแซแแแบ โบ๏ธ ..\nแแฎแแฎแแปแแบแธแแญแฏ ๐ ** `{urlissed}`", reply_to_message_id=reply_id
    )
    if not urlissed:
        await pablo.edit("แแฎแแปแแบแธแแฌแแแบแแซ แแแฑแธโแแฒแแฒแท แแฑแซแแบแธแแฑแซแแบแแญแฏแแบแกแฏแถแธแแแบ ๐!\n* แแฑแซแแบแธแแฑแซแแบแแแฌแแฒ แแแบแแฝแฑแแฌแแฑแแผแฎแธ ๐ \nVideo แแพแฌแแแบแธ \n/video music name\n{ แฅแแแฌ - /video แแฑแแแญแฏแแฒ }")
        return

    search = SearchVideos(f"{urlissed}", offset=1, mode="dict", max_results=1)
    mi = search.result()
    mio = mi["search_result"]
    mo = mio[0]["link"]
    thum = mio[0]["title"]
    fridayz = mio[0]["id"]
    mio[0]["channel"]
    kekme = f"https://img.youtube.com/vi/{fridayz}/hqdefault.jpg"
    await asyncio.sleep(0.6)
    url = mo
    sedlyf = wget.download(kekme)
    opts = {
        "format": "best",
        "addmetadata": True,
        "key": "FFmpegMetadata",
        "prefer_ffmpeg": True,
        "geo_bypass": True,
        "nocheckcertificate": True,
        "postprocessors": [{"key": "FFmpegVideoConvertor", "preferedformat": "mp4"}],
        "outtmpl": "%(id)s.mp4",
        "logtostderr": False,
        "quiet": True,
    }
    try:
        with YoutubeDL(opts) as ytdl:
            ytdl_data = ytdl.extract_info(url, download=True)
    except Exception as e:
        await event.edit(event, f"**Down แแฌแกแแแบแแแผแฑแแฐแธ ๐ญ** \n**Error :** `{str(e)}`")
        return
    c_time = time.time()
    file_stark = f"{ytdl_data['id']}.mp4"
    capy = f"""
**๐ต ๐ป๐๐๐๐ :** [{thum}]({mo})</a>\n<b>๐  แแฑแฌแแบแธแแญแฏแแฐ  : <i><b>{message.from_user.mention}</b>\n<b>๐   แแพแฌแแฑแธแแฐ     : <i><b>{message.chat.title}</b>\n๐ค Uploaded By : <a href="https://t.me/Painglay15">ยฉ  Ko Paing </a><b>\n<b><a href="https://t.me/mksviplink">ยฉ MKS Channel</a></b>
"""
    await client.send_video(
        message.chat.id, reply_to_message_id=reply_id,
        video=open(file_stark, "rb"),
        duration=int(ytdl_data["duration"]),
        file_name=str(ytdl_data["title"]),
        thumb=sedlyf,
        caption=capy,
        supports_streaming=True,
        progress=progress,
        progress_args=(
            pablo,
            c_time,
            f"**๐ฅ Down แแฑแแซแแแบ แแแแฑแฌแแทแบแแซแแฑแฌแบ ๐ ๐** ...Upload......`{urlissed}`",
            file_stark,
        ),
    )
    await pablo.delete()
    for files in (sedlyf, file_stark):
        if files and os.path.exists(files):
            os.remove(files)
            
            
 @Client.on_message(filters.text & filters.command(["lyrics"]))
async def sng(bot, message):
        if not message.reply_to_message:
          await message.reply_text("Please reply to a message")
        else:          
          mee = await message.reply_text("`Searching ๐`")
          song = message.reply_to_message.text
          chat_id = message.from_user.id
          rpl = lyrics(song)
          await mee.delete()
          try:
            await mee.delete()
            await bot.send_message(chat_id, text = rpl, reply_to_message_id = message.id, reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("แดแดแดแดแดแดs ", url = f"t.me/mkn_bots_updates")]]))
          except Exception as e:                            
             await message.reply_text(f"I Can't Find A Song With `{song}`", quote = True, reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("แดแดแดแดแดแดs", url = f"t.me/mkn_bots_updates")]]))


def search(song):
        r = requests.get(API + song)
        find = r.json()
        return find
       
def lyrics(song):
        fin = search(song)
        text = f'**๐ถ Sแดแดแดแด๊ฑ๊ฐแดสสy Exแดสแดแดแดแดแด Lyษชสษชแด๊ฑ O๊ฐ {song}**\n\n'
        text += f'`{fin["lyrics"]}`'
        text += '\n\n\n**Made By Artificial Intelligence**'
        return text
           
            
