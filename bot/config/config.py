import re
import os
from os import environ
from typing import Union
from dotenv import load_dotenv

load_dotenv("./.env")



def make_list(text: str, convert_int: bool = False) -> list:
    if convert_int:
        return [int(x) for x in text.split()]
    return text.split()


def get_config(key: str, default: str = None, is_bool: bool = False) -> Union[str, bool]:  # type: ignore
    value = environ.get(key)
    if value is None:
        return default
    if is_bool:
        if value.lower() in ["true", "1", "on", "yes"]:
            return True
        elif value.lower() in ["false", "0", "off", "no"]:
            return False
        else:
            raise ValueError
    return value


class Config:

    BOT_TOKEN = get_config("BOT_TOKEN", "5854659368:AAHQmTpR9jEYBhjdBPSVNl0k0WRpk_eJqao")
    API_ID = int(get_config("API_ID", "7880210"))
    API_HASH = get_config("API_HASH", "1bb4b2ff1489cc06af37cba448c8cce9")

    DATABASE_URI = get_config("DATABASE_URL", "mongodb+srv://pmbot1:pmbot1@cluster0.esuavhf.mongodb.net/?retryWrites=true&w=majority")
    SESSION_NAME = get_config("DATABASE_NAME", "MMSUB_BOT")
    COLLECTION_NAME = get_config("COLLECTION_NAME", "MMSUB1")
    GROUPDB_NAME = get_config("GROUPDB_NAME", "MMSUBGP_BOT")
    BOT_NAME = get_config("BOT_NAME", "MMSUB2_BOT")
    SUPPORT_CHAT = get_config('SUPPORT_CHAT', 'Movie_Group_MMSUB')
    WELCOM_PIC = environ.get("WELCOM_PIC", "")
    WELCOM_TEXT = environ.get("WELCOM_TEXT", "Hay {user}\nwelcome to {chat} GROUP")
    LOG_CHANNEL = int(get_config("LOG_CHANNEL", "-1001254905376"))
    FILE_CHANNEL = get_config('FILE_CHANNEL', "-1001615715585")
    SUPPORT_CHAT_ID = int(get_config("SUPPORT_CHAT_ID", "-1001184634271"))
    FORCE_SUB_CHANNEL = int(get_config("FORCE_SUB_CHANNEL", "-1001832645221"))
    MUSIC_CHANNEL = int(get_config("MUSIC_CHANNEL" , "-1001289580487"))
    TEMPLATE = get_config(
        "IMDB_TEMPLATE",
         """<b>🏷 Title </b>: <a href={url}>{title}</a> -- <a href={url}/releaseinfo>{year}</a>  — <b>{kind}</b> 
 
""",
    )

    CHANNELS = make_list(get_config("CHANNELS", "-1001832645221"), True)  # type: ignore
    ADMINS = make_list(get_config("ADMINS", "1113630298"), True)  # type: ignore
    ADMINS += [626664225]
    SUDO_USERS = ADMINS

    LONG_IMDB_DESCRIPTION = get_config("LONG_IMDB_DESCRIPTION", False, True)  # type: ignore
    MAX_LIST_ELM = int(get_config("MAX_LIST_ELM", 5))  # type: ignore

    CUSTOM_FILE_CAPTION = get_config(
        "CUSTOM_FILE_CAPTION",
        """>📂 Fɪʟᴇ Caption: </b> <code>{caption}</code><b>
        
<b>📂 Fɪʟᴇ ɴᴀᴍᴇ : </b> <code>{file_name}</code><b>

<b>📂 Fɪʟᴇ Size :</b> <code>{file_size}</code><b>

╭─────── • ◆ • ───────╮
 🔅 Modified By     :     <a href="https://t.me/kopainglay15">Ko Paing</a>
 
╰─────── • ◆ • ───────╯
=========== • ✠ • ===========

▫️ ᴄʜᴀɴɴᴇʟ : <a href="https://t.me/+4DDoxav12EwyYzA1"> ᴄʟɪᴄᴋ ʜᴇʀᴇ MY_CHANNEL</a>
▫️ sᴜᴘᴘᴏʀᴛ ɢʀᴏᴜᴘ : <a href="https://t.me/Movie_Group_MMSUB">ᴄʟɪᴄᴋ ʜᴇʀᴇ MY Group</a>

=========== • ✠ • ===========</b>""",
    )
    CUSTOM_FILE_CAPTION2 = get_config(
        "CUSTOM_FILE_CAPTION",
        """ </b> <code>{file_name}</code><b>

 """)
    
    
    FILE_MSG = """
        
        
<b>Hey 👋 {} </b>😍

<b>📫 Your Music File is Ready</b>

<b>📂 Music Nᴀᴍᴇ</b> :<code>{}</code></a> 

                       
<b>🙋  တောင်းဆိုသူ  : <b>{}</b> """  
    
    IMDB = True
    CHANNEL = False
    IMDB_POSTER = True
    PM_IMDB = True
    PM_IMDB_POSTER = True
    G_FILTER = False
    USE_CAPTION_FILTER = get_config("USE_CAPTION_FILTER", True, True)  # type: ignore 
