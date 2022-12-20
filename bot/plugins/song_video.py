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
from ..config import Config

import youtube_dl
import requests

def time_to_seconds(time):
    stringt = str(time)
    return sum(int(x) * 60 ** i for i, x in enumerate(reversed(stringt.split(':'))))

@Client.on_message(filters.private & filters.text & filters.incoming)
async def pm_text(bot, message):
    content = message.text
    user = message.from_user.first_name
    user_id = message.from_user.id
    if content.startswith("/") or content.startswith("#"): return  # ignore commands and hashtags
    if user_id in Config.ADMINS: return # ignore admins
    await message.reply_text("<b>Yᴏᴜʀ ᴍᴇssᴀɢᴇ ʜᴀs ʙᴇᴇɴ sᴇɴᴛ ᴛᴏ ᴍʏ ᴍᴏᴅᴇʀᴀᴛᴏʀs!\n\nသင့်စာကို မင်မင်ထံ ပေးပို့လိုက်ပါပြီး။ !</b>")
    await bot.send_message(
        chat_id=Config.LOG_CHANNEL,
        text=f"<b>#𝐏𝐌_𝐌𝐒𝐆\n\n{bot.me.username}\n\nNᴀᴍᴇ : {user}\n\nID : {user_id}\n\nMᴇssᴀɢᴇ : {content}</b>"
    )
    
@Client.on_message(filters.command(["song", "music", "mp3"]) & ~filters.channel)
def song(client, message):
    urlissed = get_text(message)
    user_id = message.from_user.id 
    user_name = message.from_user.first_name 
    rpk = "["+user_name+"](tg://user?id="+str(user_id)+")"

    query = ''
    for i in message.command[1:]:
        query += ' ' + str(i)
    print(query)
    m = message.reply(f"**🔎🔎 ရှာပေးနေပါတယ် ☺️ .. \nဒီသီချင်းကို 👉 ** `{urlissed}`")
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


        performer = f"[KO PAING]" 
        duration = results[0]["duration"]
        url_suffix = results[0]["url_suffix"]
        views = results[0]["views"]

   
    except Exception as e:
        m.edit(
            "****သီချင်းနာမည်ပါ မရေး‌ဘဲနဲ့ ခေါင်းခေါက်လိုက်အုံးမယ် 🙄!\n* ခေါင်းခေါက်ရတာလဲ လက်တွေနာနေပြီး 🌝 </a>\nMusic ရှာနည်း\n /song music name \n{ ဥပမာ - /song သေမလိုပဲ }**"
        )
        print(str(e))
        return
    m.edit("**🔎  ရှာတွေတာ တင်ပေးနေပါတယ် \nခဏစောင့်ပါနော် 😊😊... Upload......❣️**")
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(link, download=False)
            audio_file = ydl.prepare_filename(info_dict)
            ydl.process_info(info_dict)
        #rep = '**𝚂𝚄𝙱𝚂𝙲𝚁𝙸𝙱𝙴 ›› [𝙾𝙿𝚄𝚂-𝚃𝙴𝙲𝙷𝚉](https://youtube.com/channel/UCf_dVNrilcT0V2R--HbYpMA)**\n**𝙿𝙾𝚆𝙴𝚁𝙴𝙳 𝙱𝚈 ›› [muѕíc вσч](https://t.me/OPMusicBoy_Bot)**'
        
        rep = rep = f'🎵 𝑻𝒊𝒕𝒍𝒆 : [{title}]({link})\n🙋  Request By  : {rpk}\n🔎  Searching      : {message.chat.title}\n📤 Uploaded By : [©  Ko Paing](https://t.me/KOPAINGLAY15)\n[© MKS Channel](https://t.me/mksviplink2)' 
       
        secmul, dur, dur_arr = 1, 0, duration.split(':')
        for i in range(len(dur_arr)-1, -1, -1):
            dur += (int(dur_arr[i]) * secmul)
            secmul *= 60
    
    
        query += ' ' + str(i)
        print(query)    
        message.reply_audio(audio_file, caption=rep, parse_mode=enums.ParseMode.MARKDOWN, quote=False, title=title, duration=dur, performer=performer, thumb=thumb_name)
        m.delete()
    except Exception as e:
        m.edit("**🚫 𝙴𝚁𝚁𝙾𝚁 🚫**")
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
            "".join("❣️" for i in range(math.floor(percentage / 10))),
            "".join("🧐" for i in range(10 - math.floor(percentage / 10))),
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


    
@Client.on_message(filters.command(["video", "mp4"]))
async def vsong(client, message: Message):
    urlissed = get_text(message)
    query = ''
    for i in message.command[1:]:
        query += ' ' + str(i)
    print(query)
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
