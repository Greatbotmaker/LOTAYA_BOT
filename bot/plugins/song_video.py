from __future__ import unicode_literals

import os
import requests
import aiohttp
import yt_dlp
import asyncio
import math
import time

import wget
import aiofiles

from pyrogram import filters, Client, enums
from pyrogram.errors import FloodWait, MessageNotModified
from pyrogram.types import Message
from youtube_search import YoutubeSearch
from youtubesearchpython import SearchVideos
from yt_dlp import YoutubeDL
import youtube_dl
import requests

def time_to_seconds(time):
    stringt = str(time)
    return sum(int(x) * 60 ** i for i, x in enumerate(reversed(stringt.split(':'))))


@Client.on_message(filters.command(["song", "music", "mp3"]) & ~filters.channel)
def song(client, message):

    user_id = message.from_user.id 
    user_name = message.from_user.first_name 
    rpk = "["+user_name+"](tg://user?id="+str(user_id)+")"

    query = ''
    for i in message.command[1:]:
        query += ' ' + str(i)
    print(query)
    m = message.reply("**🔎🔎 ရှာပေးနေပါတယ် ☺️ .. \nဒီသီချင်းကို 👉 ** `{urlissed}`")
    ydl_opts = {"format": "bestaudio[ext=m4a]"}
    try:
        results = YoutubeSearch(query, max_results=1).to_dict()
        link = f"https://youtube.com{results[0]['url_suffix']}"
        #print(results)
        title = results[0]["title"][:40]       
        thumbnail = results[0]["thumbnails"][0]
        thumb_name = f'thumb{title}.jpg'
        thumb = requests.get(thumbnail, allow_redirects=True)
        open(thumb_name, 'wb').write(thumb.content)


        performer = f"[KO PAING LAY]" 
        duration = results[0]["duration"]
        url_suffix = results[0]["url_suffix"]
        views = results[0]["views"]

    except Exception as e:
        m.edit(
            "**သီချင်းနာမည်ပါ မရေး‌ဘဲနဲ့ ခေါင်းခေါက်လိုက်အုံးမယ် 🙄!\n* ခေါင်းခေါက်ရတာလဲ လက်တွေနာနေပြီး 🌝 </a>\nMusic ရှာနည်း\n /song music name \n{ ဥပမာ - /song သေမလိုပဲ } *")
        print(str(e))
        return
    m.edit("**dσwnlσαdíng чσur ѕσng...!**")
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(link, download=False)
            audio_file = ydl.prepare_filename(info_dict)
            ydl.process_info(info_dict)
        rep = f'🎵 <b> 𝑻𝒊𝒕𝒍𝒆:</b> <a href="{link}">{title}</a>\n<b>🙋  တောင်းဆိုသူ  : <i><b>{message.from_user.mention}</b>\n<b>🔎  ရှာပေးသူ       : <i><b>{message.chat.title}</b>\n📤 Uploaded By : <a href="https://t.me/Painglay15">©  Ko Paing </a><b>\n<b><a href="https://t.me/mksviplink">© MKS Channel</a></b>'
        secmul, dur, dur_arr = 1, 0, duration.split(':')
        for i in range(len(dur_arr)-1, -1, -1):
            dur += (int(dur_arr[i]) * secmul)
            secmul *= 60
        message.reply_audio(audio_file, caption=rep, parse_mode=enums.ParseMode.MARKDOWN, quote=False, title=title, duration=dur, performer=performer, thumb=thumb_name)
        m.delete()
    except Exception as e:
        m.edit("**ဘာမှန်းမသိတဲ့ Error လေးတက်သွားပါတယ် 🥲 ပြန်ရှာကြည့်ပါနော် \n\n@PAINGLAY15 !!**")
        print(e)

    try:
        os.remove(audio_file)
        os.remove(thumb_name)
    except Exception as e:
        print(e)

def get_text(message: Message) -> [None,str]:
    text_to_return = message.text
    if message.text is None:
        return None
    if " " not in text_to_return:
        return None
    try:
        return message.text.split(None, 1)[1]
    except IndexError:
        return None
    
    
@Client.on_message(filters.command(["video", "mp4"]))
async def vsong(client, message: Message):
    urlissed = get_text(message)

    pablo = await client.send_message(
        message.chat.id, f"**🔎🔎 ရှာပေးနေပါတယ် ☺️ ..\nဒီသီချင်းကို 👉 ** `{urlissed}`"
    )
    if not urlissed:
        await pablo.edit("သီချင်းနာမည်ပါ မရေး‌ဘဲနဲ့ ခေါင်းခေါက်လိုက်အုံးမယ် 🙄!\n* ခေါင်းခေါက်ရတာလဲ လက်တွေနာနေပြီး 🌝 \nVideo ရှာနည်း \n/video music name\n{ ဥပမာ - /video သေမလိုပဲ }")
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
        await event.edit(event,  f"**Down တာအဆင်မပြေဘူး 😭** \n**Error :**`{str(e)}`")
        return
    c_time = time.time()
    file_stark = f"{ytdl_data['id']}.mp4"
    capy = capy = f"""
**🎵 𝑻𝒊𝒕𝒍𝒆 :** [{thum}]({mo})</a>\n<b>🙋  တောင်းဆိုသူ  : <i><b>{message.from_user.mention}</b>\n<b>🔎   ရှာပေးသူ     : <i><b>{message.chat.title}</b>\n📤 Uploaded By : <a href="https://t.me/Painglay15">©  Ko Paing </a><b>\n<b><a href="https://t.me/mksviplink">© MKS Channel</a></b>
"""
    await client.send_video(
        message.chat.id,
        video=open(file_stark, "rb"),
        duration=int(ytdl_data["duration"]),
        file_name=str(ytdl_data["title"]),
        thumb=sedlyf,
        caption=capy,
        supports_streaming=True,        
        
    )
    await pablo.delete()
    for files in (sedlyf, file_stark):
        if files and os.path.exists(files):
            os.remove(files)
