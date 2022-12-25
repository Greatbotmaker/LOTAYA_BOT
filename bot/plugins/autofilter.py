from __future__ import unicode_literals


import asyncio
import time
import requests 
import aiofiles
import aiohttp
import wget
import math
import re
import pyrogram
import random
import os
import youtube_dl
import asyncio, re, ast, math, logging
import yt_dlp
from gtts import gTTS
from info import info
from info import PICS, PICS2, DOWNLOAD_LOCATION
from bot import Bot
from googletrans import Translator
from bot.kopaing.helper.list import list
from telegraph import upload_file
from gutils import get_file_id

from bot.kopaing.helper.fotnt_string import Fonts
from bot.kopaing.helper.admin_check import admin_check, admin_fliter
from bot.kopaing.helper.extract import extract_time, extract_user
import traceback
from asyncio import get_running_loop
from io import BytesIO
from googletrans import Translator
from gtts import gTTS
from time import time, sleep
from datetime import datetime
from pytz import timezone
from pyrogram.errors.exceptions.forbidden_403 import ChatWriteForbidden
from pyrogram.errors.exceptions.bad_request_400 import ChatAdminRequired, UserAdminInvalid
from pyrogram.errors import FloodWait, MessageNotModified
from youtubesearchpython import SearchVideos
from yt_dlp import YoutubeDL
from youtube_search import YoutubeSearch

from pyrogram import filters, Client as Sflix
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, Message, ChatPermissions, User, Message, Document 
from pyrogram import Client, enums, errors, filters, types
from ..database.gfilters_mdb import find_gfilter, get_gfilters
from ..config import Config
from ..database import a_filter
from ..database import configDB as config_db
from ..utils.botTools import check_fsub, format_buttons, get_size, parse_link
from ..utils.cache import Cache
from ..utils.imdbHelpers import get_poster
from ..utils.logger import LOGGER

TIMEZONE = (os.environ.get("TIMEZONE", "Asia/Yangon"))
log = LOGGER(__name__)
logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)

Thanks = """ Thats The End Of Your Audio Book, And Thanks for Using this Service"""

curr = datetime.now(timezone(TIMEZONE))
date = curr.strftime('%d %B, %Y')
time = curr.strftime('%I:%M:%S %p')
G_MODE = {}



@Bot.on_message(filters.group & filters.text & filters.incoming, group=-1)  # type: ignore
async def give_filter(bot: Bot, message: types.Message):
    await global_filters(bot, message) 


    if message.text.startswith("/"):
        return  # ignore commands

    if re.findall("((^\/|^,|^!|^\.|^[\U0001F600-\U000E007F]).*)", message.text):  # type: ignore
        return

    if 2 < len(message.text) < 100:
        search = message.text
        files, offset, total_results = await a_filter.get_search_results(
            search.lower(), offset=0, filter=True
        )
        if not files:
            return
    else:
        return
    key = f"{message.chat.id}-{message.id}"

    Cache.BUTTONS[key] = search
    settings = await config_db.get_settings(f"SETTINGS_{message.chat.id}")
    if settings["IMDB"]:  # type: ignore
        imdb = await get_poster(search, file=(files[0])["file_name"])
    else:
        imdb = {}
    Cache.SEARCH_DATA[key] = files, offset, total_results, imdb, settings
    if not settings.get("DOWNLOAD_BUTTON"):  # type: ignore
        btn = await format_buttons(files, settings["CHANNEL"])  # type: ignore
        if offset != "":
            req = message.from_user.id if message.from_user else 0
            btn.append(
                [
                    types.InlineKeyboardButton(
                        text=f"🔰 1/{math.ceil(int(total_results) / 10)} 🔰", callback_data="pages"
                    ),
                    types.InlineKeyboardButton(
                        text="NEXT ⏩", callback_data=f"next_{req}_{key}_{offset}"
                    ),
                ]
                )
            
            
        else:
                       
            btn.append([types.InlineKeyboardButton(text="𝐍𝐎 𝐌𝐎𝐑𝐄 𝐏𝐀𝐆𝐄𝐒 𝐀𝐕𝐀𝐈𝐋𝐀𝐁𝐋𝐄",callback_data="pages")])
           
    else:
        btn = [
            [
                types.InlineKeyboardButton(
                    "D༙O༙W༙N༙L༙O༙A༙D༙", url=f"https://t.me/{bot.me.username}?start=filter{key}"
                )
            ]
        ]

    if imdb:
        cap = Config.TEMPLATE.format(  # type: ignore
            query=search,
            **imdb,
            **locals(),
        )
    else:
	
        cap = f"🔎 𝙌𝙪𝙚𝙧𝙮 : {search}"
    if imdb and imdb.get("poster") and settings["IMDB_POSTER"]:  # type: ignore
        try:
	
            await message.reply_photo(
                photo=imdb.get("poster"),  # type: ignore
                caption=cap[:1024],
                reply_markup=types.InlineKeyboardMarkup(btn),
                quote=True,				   
            )
        except (errors.MediaEmpty, errors.PhotoInvalidDimensions, errors.WebpageMediaEmpty):
            pic = imdb.get("poster")
            poster = pic.replace(".jpg", "._V1_UX360.jpg")
            await message.reply_photo(
                photo=poster,
                caption=cap[:1024],
                reply_markup=types.InlineKeyboardMarkup(btn),
                quote=True,
            )
        except Exception as e:
            log.exception(e)
            await message.reply_text(cap, reply_markup=types.InlineKeyboardMarkup(btn), quote=True)
    else:
        await message.reply_photo(
            photo=random.choice(PICS2),
            caption=cap,
            reply_markup=types.InlineKeyboardMarkup(btn),
            quote=True)       
       


@Bot.on_callback_query(filters.regex(r"^next"))  # type: ignore
async def next_page(bot: Bot, query: types.CallbackQuery):
    _, req, key, offset = query.data.split("_")  # type: ignore
    if int(req) not in [query.from_user.id, 0]:
        return await query.answer("🙄 ဟင်းဟင်း သူများရိုက်ထားတာလေ \n\n😎  နှိပ်ချင်ရင် ဂရုထဲ ကွကိုရိုက်ပါ 😎!!\n\nUploaded By :Ko Paing ❣️!", show_alert=True)
    try:
        offset = int(offset)
    except:
        offset = 0
    search = Cache.BUTTONS.get(key)
    if not search:
        await query.answer(
            "Search Expired\nPlease send movie name again.\n\nရှာဖွေမှု သက်တမ်းကုန်သွားပါပြီ။\nကျေးဇူးပြု၍ ရုပ်ရှင်အမည်ကို \nGroup ထဲ‌တွင် ထပ်မံပေးပို့ပါ။\n\n**@Movie_Group_MMSUB** ", show_alert=True
        )
        return

    files, n_offset, total = await a_filter.get_search_results(search, offset=offset, filter=True)
    try:
        n_offset = int(n_offset)
    except:
        n_offset = 0

    if not files:
        return
    settings = await config_db.get_settings(f"SETTINGS_{query.message.chat.id}")

    btn = await format_buttons(files, settings["CHANNEL"])  # type: ignore

    if 0 < offset <= 6:
        off_set = 0
    elif offset == 0:
        off_set = None
    else:
        off_set = offset - 10
    if n_offset == 0:
        btn.append(
            [
                types.InlineKeyboardButton("⏪ BACK", callback_data=f"next_{req}_{key}_{off_set}"),
                types.InlineKeyboardButton(
                    f"🔰 Pages {math.ceil(int(offset) / 10) + 1} / {math.ceil(total / 10)} 🔰",
                    callback_data="pages",
                ),
            ]
        )
        
        
    elif off_set is None:
        btn.append(
            [
                types.InlineKeyboardButton(
                    f"🔰 {math.ceil(int(offset) / 10) + 1} / {math.ceil(total / 10)} 🔰",
                    callback_data="pages",
                ),
                types.InlineKeyboardButton("NEXT ⏩", callback_data=f"next_{req}_{key}_{n_offset}"),
            ]
        )
        
    else:
        btn.append(
            [
                types.InlineKeyboardButton("⏪ BACK", callback_data=f"next_{req}_{key}_{off_set}"),
                types.InlineKeyboardButton(
                    f"🔰 {math.ceil(int(offset) / 10) + 1} / {math.ceil(total / 10)} 🔰",
                    callback_data="pages",
                ),
                types.InlineKeyboardButton("NEXT ⏩", callback_data=f"next_{req}_{key}_{n_offset}"),
            ],
        )
        
    try:
        await query.edit_message_reply_markup(reply_markup=types.InlineKeyboardMarkup(btn))
    except errors.MessageNotModified:
        pass
    await query.answer()


@Bot.on_callback_query(filters.regex("^file"))  # type: ignore
async def handle_file(bot: Bot, query: types.CallbackQuery):
            
    _, file_id = query.data.split()
    file_info = await a_filter.get_file_details(file_id)  # type: ignore
    if not file_info:
        return await query.answer("FileNotFoundError", True)
    query.message.from_user = query.from_user
    isMsg = query.message.chat.type == enums.ChatType.PRIVATE
    if not await check_fsub(bot, query.message, sendMsg=isMsg):
        if not isMsg:
            return await query.answer(url=f"https://t.me/{bot.me.username}?start=fsub")
        return await query.answer("Please Join My Update Channel and click again")
    try:
        await bot.send_cached_media(
            query.from_user.id,
            file_id,  # type: ignore
            caption=Config.CUSTOM_FILE_CAPTION.format(  # type: ignore
                file_name=file_info["file_name"],
                file_size=get_size(file_info["file_size"]),
                caption=file_info["caption"],
            ),
                reply_markup=types.InlineKeyboardMarkup(
            [
                [
                    types.InlineKeyboardButton('Sᴜᴘᴘᴏʀᴛ Gʀᴏᴜᴘ', url="https://t.me/Movie_Group_MMSUB"),             
                    types.InlineKeyboardButton('Uᴘᴅᴀᴛᴇs Cʜᴀɴɴᴇʟ', url="https://t.me/+4DDoxav12EwyYzA1")
                ],           
                [
                    types.InlineKeyboardButton("⭕️ Owner Acc ⭕", url="https://t.me/KOPAINGLAY15")
                ]
            ]

        ),
            reply_to_message_id=query.message.id,
        )
        await bot.send_message(chat_id=query.from_user.id, text=f"👋 Hello {query.from_user.mention},Happy Downloading and Come Again... \n\n ပျော်ရွှင်စွာဒေါင်းလုဒ်လုပ်ပြီး ‌နောက်ထပ်လာခဲ့ပါ... \n\n👉🏻 @Movie_Group_MMSUB❤️")        
        await bot.send_cached_media(
                Config.FILE_CHANNEL,
                file_id,
                caption=Config.CUSTOM_FILE_CAPTION2.format(  # type: ignore
                file_name=file_info["file_name"],
                file_size=get_size(file_info["file_size"]),
                caption=file_info["caption"],
            ),
                protect_content=True,
                reply_to_message_id=query.message.id,
        )
          
		
    except errors.PeerIdInvalid:
        return await query.answer(f"https://t.me/{bot.me.username}?start=okok")
    await query.answer(f'Sending :Check bot DM \n\n {file_info["file_name"]}', show_alert=True)





#-----------------------------------------------------------------------------------------------
@Client.on_message(filters.command('g_filter') & filters.group & admin_fliter)
async def global_filters(client, message): 
      mode_on = ["yes", "on", "true"]
      mode_of = ["no", "off", "false"]

      try: 
         args = message.text.split(None, 1)[1].lower() 
      except: 
         return await message.reply("**𝙸𝙽𝙲𝙾𝙼𝙿𝙻𝙴𝚃𝙴 𝙲𝙾𝙼𝙼𝙰𝙽𝙳...**")
      
      m = await message.reply("**𝚂𝙴𝚃𝚃𝙸𝙽𝙶.../**")

      if args in mode_on:
          G_MODE[str(message.chat.id)] = "True" 
          await m.edit("**𝙶𝙻𝙾𝙱𝙰𝙻 𝙴𝙽𝙰𝙱𝙻𝙴𝙳**")
      
      elif args in mode_of:
          G_MODE[str(message.chat.id)] = "False"
          await m.edit("**𝙶𝙻𝙾𝙱𝙰𝙻 𝙳𝙸𝚂𝙰𝙱𝙻𝙴𝙳**")
      else:
          await m.edit("𝚄𝚂𝙴 :- /g_filter on 𝙾𝚁 /g_filter off")
		
		

async def global_filters(bot: Client, message, text=False):
    group_id = message.chat.id
    name = text or message.text
    reply_id = message.reply_to_message.id if message.reply_to_message else message.id
    keywords = await get_gfilters('gfilters')
    for keyword in reversed(sorted(keywords, key=len)):
        pattern = r"( |^|[^\w])" + re.escape(keyword) + r"( |$|[^\w])"
        if re.search(pattern, name, flags=re.IGNORECASE):
            reply_text, btn, alert, fileid = await find_gfilter('gfilters', keyword)

            if reply_text:
                reply_text = reply_text.replace("\\n", "\n").replace("\\t", "\t")

            if btn is not None:
                try:
                    if fileid == "None":
                        if btn == "[]":
                            knd3 = await bot.send_message(
                                group_id, 
                                reply_text, 
                                disable_web_page_preview=True,
                                reply_to_message_id=reply_id
                            )
                       

                        else:
                            button = eval(btn)
                            knd2 = await bot.send_message(
                                group_id,
                                reply_text,
                                disable_web_page_preview=True,
                                reply_markup=InlineKeyboardMarkup(button),
                                reply_to_message_id=reply_id
                            )
                         

                    elif btn == "[]":
                        knd1 = await bot.send_cached_media(
                            group_id,
                            fileid,
                            caption=reply_text or "",
                            reply_to_message_id=reply_id
                        )
                    

                    else:
                        button = eval(btn)
                        knd = await message.reply_cached_media(
                            fileid,
                            caption=reply_text or "",
                            reply_markup=InlineKeyboardMarkup(button),
                            reply_to_message_id=reply_id
                        )
                  

                except Exception as e:
                    logger.exception(e)
                break
    else:
        return False



                        #await asyncio.sleep(IMDB_DELET_TIME)
                        #await knd.delete()
                        #await message.delete()
                           


#-------------------------------------------------------------------------                

@Client.on_message(filters.command(["stickerid"]))
async def stickerid(bot, message):   
    if message.reply_to_message.sticker:
       await message.reply(f"**Sticker ID is**  \n `{message.reply_to_message.sticker.file_id}` \n \n ** Unique ID is ** \n\n`{message.reply_to_message.sticker.file_unique_id}`", quote=True)
    else: 
       await message.reply("Oops !! Not a sticker file")



#----------------------------------------------------------------------------------------    
    
@Client.on_message(filters.private & filters.command(["font"]))
async def style_buttons(c, m, cb=False):
    buttons = [[
        types.InlineKeyboardButton('𝚃𝚢𝚙𝚎𝚠𝚛𝚒𝚝𝚎𝚛', callback_data='style+typewriter'),
        types.InlineKeyboardButton('𝕆𝕦𝕥𝕝𝕚𝕟𝕖', callback_data='style+outline'),
        types.InlineKeyboardButton('𝐒𝐞𝐫𝐢𝐟', callback_data='style+serif'),
        ],[
        types.InlineKeyboardButton('𝑺𝒆𝒓𝒊𝒇', callback_data='style+bold_cool'),
        types.InlineKeyboardButton('𝑆𝑒𝑟𝑖𝑓', callback_data='style+cool'),
        types.InlineKeyboardButton('Sᴍᴀʟʟ Cᴀᴘs', callback_data='style+small_cap'),
        ],[
        types.InlineKeyboardButton('𝓈𝒸𝓇𝒾𝓅𝓉', callback_data='style+script'),
        types.InlineKeyboardButton('𝓼𝓬𝓻𝓲𝓹𝓽', callback_data='style+script_bolt'),
        types.InlineKeyboardButton('ᵗⁱⁿʸ', callback_data='style+tiny'),
        ],[
        types.InlineKeyboardButton('ᑕOᗰIᑕ', callback_data='style+comic'),
        types.InlineKeyboardButton('𝗦𝗮𝗻𝘀', callback_data='style+sans'),
        types.InlineKeyboardButton('𝙎𝙖𝙣𝙨', callback_data='style+slant_sans'),
        ],[
        types.InlineKeyboardButton('𝘚𝘢𝘯𝘴', callback_data='style+slant'),
        types.InlineKeyboardButton('𝖲𝖺𝗇𝗌', callback_data='style+sim'),
        types.InlineKeyboardButton('Ⓒ︎Ⓘ︎Ⓡ︎Ⓒ︎Ⓛ︎Ⓔ︎Ⓢ︎', callback_data='style+circles')
        ],[
        types.InlineKeyboardButton('🅒︎🅘︎🅡︎🅒︎🅛︎🅔︎🅢︎', callback_data='style+circle_dark'),
        types.InlineKeyboardButton('𝔊𝔬𝔱𝔥𝔦𝔠', callback_data='style+gothic'),
        types.InlineKeyboardButton('𝕲𝖔𝖙𝖍𝖎𝖈', callback_data='style+gothic_bolt'),
        ],[
        types.InlineKeyboardButton('C͜͡l͜͡o͜͡u͜͡d͜͡s͜͡', callback_data='style+cloud'),
        types.InlineKeyboardButton('H̆̈ă̈p̆̈p̆̈y̆̈', callback_data='style+happy'),
        types.InlineKeyboardButton('S̑̈ȃ̈d̑̈', callback_data='style+sad'),
        ],[
        types.InlineKeyboardButton('Next ➡️', callback_data="nxt")
    ]]
    if not cb:
        if ' ' in m.text:
            title = m.text.split(" ", 1)[1]
            await m.reply_text(title, reply_markup=types.InlineKeyboardMarkup(buttons), reply_to_message_id=m.id)                     
        else:
            await m.reply_text(text="Ente Any Text Eg:- `/font [text]`")    
    else:
        await m.answer()
        await m.message.edit_reply_markup(types.InlineKeyboardMarkup(buttons))


@Client.on_callback_query(filters.regex('^nxt'))
async def nxt(c, m):
    if m.data == "nxt":
        buttons = [[
            types.InlineKeyboardButton('🇸 🇵 🇪 🇨 🇮 🇦 🇱 ', callback_data='style+special'),
            types.InlineKeyboardButton('🅂🅀🅄🄰🅁🄴🅂', callback_data='style+squares'),
            types.InlineKeyboardButton('🆂︎🆀︎🆄︎🅰︎🆁︎🅴︎🆂︎', callback_data='style+squares_bold'),
            ],[
            types.InlineKeyboardButton('ꪖꪀᦔꪖꪶꪊᥴ𝓲ꪖ', callback_data='style+andalucia'),
            types.InlineKeyboardButton('爪卂几ᘜ卂', callback_data='style+manga'),
            types.InlineKeyboardButton('S̾t̾i̾n̾k̾y̾', callback_data='style+stinky'),
            ],[
            types.InlineKeyboardButton('B̥ͦu̥ͦb̥ͦb̥ͦl̥ͦe̥ͦs̥ͦ', callback_data='style+bubbles'),
            types.InlineKeyboardButton('U͟n͟d͟e͟r͟l͟i͟n͟e͟', callback_data='style+underline'),
            types.InlineKeyboardButton('꒒ꍏꀷꌩꌃꀎꁅ', callback_data='style+ladybug'),
            ],[
            types.InlineKeyboardButton('R҉a҉y҉s҉', callback_data='style+rays'),
            types.InlineKeyboardButton('B҈i҈r҈d҈s҈', callback_data='style+birds'),
            types.InlineKeyboardButton('S̸l̸a̸s̸h̸', callback_data='style+slash'),
            ],[
            types.InlineKeyboardButton('s⃠t⃠o⃠p⃠', callback_data='style+stop'),
            types.InlineKeyboardButton('S̺͆k̺͆y̺͆l̺͆i̺͆n̺͆e̺͆', callback_data='style+skyline'),
            types.InlineKeyboardButton('A͎r͎r͎o͎w͎s͎', callback_data='style+arrows'),
            ],[
            types.InlineKeyboardButton('ዪሀክቿነ', callback_data='style+qvnes'),
            types.InlineKeyboardButton('S̶t̶r̶i̶k̶e̶', callback_data='style+strike'),
            types.InlineKeyboardButton('F༙r༙o༙z༙e༙n༙', callback_data='style+frozen')
            ],[
            types.InlineKeyboardButton('⬅️ Back', callback_data='nxt+0')
        ]]
        await m.answer()
        await m.message.edit_reply_markup(types.InlineKeyboardMarkup(buttons))
    else:
        await style_buttons(c, m, cb=True)


@Client.on_callback_query(filters.regex('^style'))
async def style(c, m):
    await m.answer()
    cmd, style = m.data.split('+')

    if style == 'typewriter':
        cls = Fonts.typewriter
    if style == 'outline':
        cls = Fonts.outline
    if style == 'serif':
        cls = Fonts.serief
    if style == 'bold_cool':
        cls = Fonts.bold_cool
    if style == 'cool':
        cls = Fonts.cool
    if style == 'small_cap':
        cls = Fonts.smallcap
    if style == 'script':
        cls = Fonts.script
    if style == 'script_bolt':
        cls = Fonts.bold_script
    if style == 'tiny':
        cls = Fonts.tiny
    if style == 'comic':
        cls = Fonts.comic
    if style == 'sans':
        cls = Fonts.san
    if style == 'slant_sans':
        cls = Fonts.slant_san
    if style == 'slant':
        cls = Fonts.slant
    if style == 'sim':
        cls = Fonts.sim
    if style == 'circles':
        cls = Fonts.circles
    if style == 'circle_dark':
        cls = Fonts.dark_circle
    if style == 'gothic':
        cls = Fonts.gothic
    if style == 'gothic_bolt':
        cls = Fonts.bold_gothic
    if style == 'cloud':
        cls = Fonts.cloud
    if style == 'happy':
        cls = Fonts.happy
    if style == 'sad':
        cls = Fonts.sad
    if style == 'special':
        cls = Fonts.special
    if style == 'squares':
        cls = Fonts.square
    if style == 'squares_bold':
        cls = Fonts.dark_square
    if style == 'andalucia':
        cls = Fonts.andalucia
    if style == 'manga':
        cls = Fonts.manga
    if style == 'stinky':
        cls = Fonts.stinky
    if style == 'bubbles':
        cls = Fonts.bubbles
    if style == 'underline':
        cls = Fonts.underline
    if style == 'ladybug':
        cls = Fonts.ladybug
    if style == 'rays':
        cls = Fonts.rays
    if style == 'birds':
        cls = Fonts.birds
    if style == 'slash':
        cls = Fonts.slash
    if style == 'stop':
        cls = Fonts.stop
    if style == 'skyline':
        cls = Fonts.skyline
    if style == 'arrows':
        cls = Fonts.arrows
    if style == 'qvnes':
        cls = Fonts.rvnes
    if style == 'strike':
        cls = Fonts.strike
    if style == 'frozen':
        cls = Fonts.frozen

    r, oldtxt = m.message.reply_to_message.text.split(None, 1) 
    new_text = cls(oldtxt)            
    try:
        await m.message.edit_text(f"`{new_text}`\n\n👆 Click To Copy", reply_markup=m.message.reply_markup)
    except Exception as e:
        print(e)
        
        
        
#------------------------------------------------ban-------------------------------------------------------------------

                             
                           
@Client.on_message(filters.command("ban"))
async def ban_user(_, message):
    is_admin = await admin_check(message)
    if not is_admin:
        return 
    user_id, user_first_name = extract_user(message)
    try:
        await message.chat.ban_member(user_id=user_id)
    except Exception as error:
        await message.reply_text(str(error))                    
    else:
        if str(user_id).lower().startswith("@"):
            await message.reply_text(f"Someone else is dusting off..! \n{user_first_name} \nIs forbidden.")                              
        else:
            await message.reply_text(f"Someone else is dusting off..! \n<a href='tg://user?id={user_id}'>{user_first_name}</a> Is forbidden")                      
            

@Client.on_message(filters.command("tban"))
async def temp_ban_user(_, message):
    is_admin = await admin_check(message)
    if not is_admin:
        return
    if not len(message.command) > 1:
        return
    user_id, user_first_name = extract_user(message)
    until_date_val = extract_time(message.command[1])
    if until_date_val is None:
        return await message.reply_text(text=f"Invalid time type specified. \nExpected m, h, or d, Got it: {message.command[1][-1]}")   
    try:
        await message.chat.ban_member(user_id=user_id, until_date=until_date_val)            
    except Exception as error:
        await message.reply_text(str(error))
    else:
        if str(user_id).lower().startswith("@"):
            await message.reply_text(f"Someone else is dusting off..!\n{user_first_name}\nbanned for {message.command[1]}!")
        else:
            await message.reply_text(f"Someone else is dusting off..!\n<a href='tg://user?id={user_id}'>Lavane</a>\n banned for {message.command[1]}!")
                
                
                
#--------------------------umte----unban------------- 

@Bot.on_message(filters.command(["unban", "unmute"]))
async def un_ban_user(_, message):
    is_admin = await admin_check(message)
    if not is_admin:
        return
    user_id, user_first_name = extract_user(message)
    try:
        await message.chat.unban_member(user_id=user_id)
    except Exception as error:
        await message.reply_text(str(error))
    else:
        if str(user_id).lower().startswith("@"):
            await message.reply_text(
                "Okay, changed ... now "
                f"{user_first_name} To "
                " You can join the group!"
            )
        else:
            await message.reply_text(
                "Okay, changed ... now "
                f"<a href='tg://user?id={user_id}'>"
                f"{user_first_name}"
                "</a> To "
                " You can join the group!"
            )
            
                
@Bot.on_message(filters.command("mute"))
async def mute_user(_, message):
    is_admin = await admin_check(message)
    if not is_admin:
        return
    user_id, user_first_name = extract_user(message)
    try:
        await message.chat.restrict_member(
            user_id=user_id,
            permissions=ChatPermissions(
            )
        )
    except Exception as error:
        await message.reply_text(
            str(error)
        )
    else:
        if str(user_id).lower().startswith("@"):
            await message.reply_text(
                "👍🏻 "
                f"{user_first_name}"
                " Lavender's mouth is shut! 🤐"
            )
        else:
            await message.reply_text(
                "👍🏻 "
                f"<a href='tg://user?id={user_id}'>"
                "Of lavender"
                "</a>"
                " The mouth is closed! 🤐"
            )


@Bot.on_message(filters.command("tmute"))
async def temp_mute_user(_, message):
    is_admin = await admin_check(message)
    if not is_admin:
        return

    if not len(message.command) > 1:
        return

    user_id, user_first_name = extract_user(message)

    until_date_val = extract_time(message.command[1])
    if until_date_val is None:
        await message.reply_text(
            (
                "Invalid time type specified. "
                "Expected m, h, or d, Got it: {}"
            ).format(
                message.command[1][-1]
            )
        )
        return

    try:
        await message.chat.restrict_member(
            user_id=user_id,
            permissions=ChatPermissions(
            ),
            until_date=until_date_val
        )
    except Exception as error:
        await message.reply_text(
            str(error)
        )
    else:
        if str(user_id).lower().startswith("@"):
            await message.reply_text(
                "Be quiet for a while! 😠"
                f"{user_first_name}"
                f" muted for {message.command[1]}!"
            )
        else:
            await message.reply_text(
                "Be quiet for a while! 😠"
                f"<a href='tg://user?id={user_id}'>"
                "Of lavender"
                "</a>"
                " Mouth "
                f" muted for {message.command[1]}!"
            )


#----------------------pin---------------------------------------

@Bot.on_message(filters.command("pin") & admin_fliter)
async def pin(_, message: Message):
    if not message.reply_to_message:
        return
    await message.reply_to_message.pin()


@Bot.on_message(filters.command("unpin") & admin_fliter)             
async def unpin(_, message: Message):
    if not message.reply_to_message:
        return
    await message.reply_to_message.unpin()


    
#-------------------------------------------------kick-------------------------    

@Client.on_message(filters.group & filters.command('inkick'))
def inkick(client, message):
  user = client.get_chat_member(message.chat.id, message.from_user.id)
  if user.status in (enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER):
    if len(message.command) > 1:
      input_str = message.command
      sent_message = message.reply_text(info.START_KICK)
      sleep(20)
      sent_message.delete()
      message.delete()
      count = 0
      for member in client.get_chat_members(message.chat.id):
        if member.user.status in input_str and not member.status in (enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER):
          try:
            client.ban_chat_member(message.chat.id, member.user.id, int(time() + 45))
            count += 1
            sleep(1)
          except (ChatAdminRequired, UserAdminInvalid):
            sent_message.edit(info.ADMIN_REQUIRED)
            client.leave_chat(message.chat.id)
            break
          except FloodWait as e:
            sleep(e.x)
      try:
        sent_message.edit(info.KICKED.format(count))
      except ChatWriteForbidden:
        pass
    else:
      message.reply_text(info.INPUT_REQUIRED)
  else:
    sent_message = message.reply_text(info.CREATOR_REQUIRED)
    sleep(5)
    sent_message.delete()
    message.delete()


@Client.on_message(filters.group & filters.command('dkick'))
def dkick(client, message):
  user = client.get_chat_member(message.chat.id, message.from_user.id)
  if user.status in (enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER):
    sent_message = message.reply_text(info.START_KICK)
    sleep(20)
    sent_message.delete()
    message.delete()
    count = 0
    for member in client.get_chat_members(message.chat.id):
      if member.user.is_deleted and not member.status in (enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER):
        try:
          client.ban_chat_member(message.chat.id, member.user.id, int(time() + 45))
          count += 1
          sleep(1)
        except (ChatAdminRequired, UserAdminInvalid):
          sent_message.edit(info.ADMIN_REQUIRED)
          client.leave_chat(message.chat.id)
          break
        except FloodWait as e:
          sleep(e.x)
    try:
      sent_message.edit(info.DKICK.format(count))
    except ChatWriteForbidden:
      pass
  else:
    sent_message = message.reply_text(info.CREATOR_REQUIRED)
    sleep(5)
    sent_message.delete()
    message.delete()

  
@Client.on_message((filters.channel | filters.group) & filters.command('instatus'))
def instatus(client, message):
    sent_message = message.reply_text("🔁 Processing.....")
    recently = 0
    within_week = 0
    within_month = 0
    long_time_ago = 0
    deleted_acc = 0
    uncached = 0
    bot = 0
    for member in client.get_chat_members(message.chat.id, limit=int(10000)):
      user = member.user
      if user.is_deleted:
        deleted_acc += 1
      elif user.is_bot:
        bot += 1
      elif user.status == enums.UserStatus.RECENTLY:
        recently += 1
      elif user.status == enums.UserStatus.LAST_WEEK:
        within_week += 1
      elif user.status == enums.UserStatus.LAST_MONTH:
        within_month += 1
      elif user.status == enums.UserStatus.LONG_AGO:
        long_time_ago += 1
      else:
        uncached += 1

    chat_type = message.chat.type
    if chat_type == enums.ChatType.CHANNEL:
         sent_message.edit(f"{message.chat.title}\nChat Member Status\n\nRecently - {recently}\nWithin Week - {within_week}\nWithin Month - {within_month}\nLong Time Ago - {long_time_ago}\n\nDeleted Account - {deleted_acc}\nBot - {bot}\nUnCached - {uncached}")            
    elif chat_type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        user = client.get_chat_member(message.chat.id, message.from_user.id)
        if user.status in (enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER, Config.ADMINS):
            sent_message.edit(f"{message.chat.title}\nChat Member Status\n\nRecently - {recently}\nWithin Week - {within_week}\nWithin Month - {within_month}\nLong Time Ago - {long_time_ago}\n\nDeleted Account - {deleted_acc}\nBot - {bot}\nUnCached - {uncached}")
        else:
            sent_message.edit("you are not administrator in this chat")


#--------------------purge------------



@Bot.on_message(filters.command("purge") & (filters.group | filters.channel))                   
async def purge(client, message):
    if message.chat.type not in ((enums.ChatType.SUPERGROUP, enums.ChatType.CHANNEL)):
        return
    is_admin = await admin_check(message)
    if not is_admin:
        return

    status_message = await message.reply_text("...", quote=True)
    await message.delete()
    message_ids = []
    count_del_etion_s = 0

    if message.reply_to_message:
        for a_s_message_id in range(message.reply_to_message.id, message.id):
            message_ids.append(a_s_message_id)
            if len(message_ids) == "100":
                await client.delete_messages(
                    chat_id=message.chat.id,
                    message_ids=message_ids,
                    revoke=True
                )
                count_del_etion_s += len(message_ids)
                message_ids = []
        if len(message_ids) > 0:
            await client.delete_messages(
                chat_id=message.chat.id,
                message_ids=message_ids,
                revoke=True
            )
            count_del_etion_s += len(message_ids)
    await status_message.edit_text(f"deleted {count_del_etion_s} messages")
    await asyncio.sleep(5)
    await status_message.delete()
    
    
    
#---------------------------telegraph---------------------


@Client.on_message(filters.command("telegraph") & filters.private)
async def telegraph_upload(bot, update):
    replied = update.reply_to_message
    if not replied:
        await update.reply_text("𝚁𝙴𝙿𝙻𝚈 𝚃𝙾 𝙰 𝙿𝙷𝙾𝚃𝙾 𝙾𝚁 𝚅𝙸𝙳𝙴𝙾 𝚄𝙽𝙳𝙴𝚁 𝟻𝙼𝙱.")
        return
    file_info = get_file_id(replied)
    if not file_info:
        await update.reply_text("Not supported!")
        return
    text = await update.reply_text(text="<code>Downloading to My Server ...</code>", disable_web_page_preview=True)   
    media = await update.reply_to_message.download()   
    await text.edit_text(text="<code>Downloading Completed. Now I am Uploading to telegra.ph Link ...</code>", disable_web_page_preview=True)                                            
    try:
        response = upload_file(media)
    except Exception as error:
        print(error)
        await text.edit_text(text=f"Error :- {error}", disable_web_page_preview=True)       
        return    
    try:
        os.remove(media)
    except Exception as error:
        print(error)
        return    
    await text.edit_text(
        text=f"<b>Link :-</b>\n\n<code>https://graph.org{response[0]}</code>",
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup( [[
            InlineKeyboardButton(text="Open Link", url=f"https://graph.org{response[0]}"),
            InlineKeyboardButton(text="Share Link", url=f"https://telegram.me/share/url?url=https://graph.org{response[0]}")
            ],[
            InlineKeyboardButton(text="✗ Close ✗", callback_data="close")
            ]])
        )
    
#---------------------tts----------------





def convert(text):
    audio = BytesIO()
    i = Translator().translate(text, dest="en")
    lang = i.src
    tts = gTTS(text, lang=lang)
    audio.name = lang + ".mp3"
    tts.write_to_fp(audio)
    return audio


@Client.on_message(filters.command("tts"))
async def text_to_speech(_, message: Message):
    if not message.reply_to_message:
        return await message.reply_text("Reply to some text ffs.")
    if not message.reply_to_message.text:
        return await message.reply_text("Reply to some text ffs.")
    m = await message.reply_text("Processing")
    text = message.reply_to_message.text
    try:
        loop = get_running_loop()
        audio = await loop.run_in_executor(None, convert, text)
        await message.reply_audio(audio)
        await m.delete()
        audio.close()
    except Exception as e:
        await m.edit(e)
        e = traceback.format_exc()
        print(e)


#---------------song------------

            
#------------------------------



@Client.on_message(filters.command(["tr"]))
async def left(client,message):
	if (message.reply_to_message):
		try:
			lgcd = message.text.split("/tr")
			lg_cd = lgcd[1].lower().replace(" ", "")
			tr_text = message.reply_to_message.text
			translator = Translator()
			translation = translator.translate(tr_text,dest = lg_cd)
			hehek = InlineKeyboardMarkup(
                                [
                                    [
                                        InlineKeyboardButton(
                                            text=f"𝘔𝘰𝘳𝘦 𝘓𝘢𝘯𝘨 𝘊𝘰𝘥𝘦𝘴", url="https://cloud.google.com/translate/docs/languages"
                                        )
                                    ],
				    [
                                        InlineKeyboardButton(
                                            "𝘊𝘭𝘰𝘴𝘦", callback_data="close_data"
                                        )
                                    ],
                                ]
                            )
			try:
				for i in list:
					if list[i]==translation.src:
						fromt = i
					if list[i] == translation.dest:
						to = i 
				await message.reply_text(f"translated from {fromt.capitalize()} to {to.capitalize()}\n\n```{translation.text}```", reply_markup=hehek, quote=True)
			except:
			   	await message.reply_text(f"Translated from **{translation.src}** To **{translation.dest}**\n\n```{translation.text}```", reply_markup=hehek, quote=True)
			

		except :
			print("error")
	else:
			 ms = await message.reply_text("You can Use This Command by using reply to message")
			 await ms.delete()
            


#-------------------

@Client.on_message(filters.command(["audiobook"])) # PdfToText 
async def pdf_to_text(bot, message):
 try:
           if message.reply_to_message:
                pdf_path = DOWNLOAD_LOCATION + f"{message.chat.id}.pdf" #pdfFileObject
                txt = await message.reply("Downloading.....")
                await message.reply_to_message.download(pdf_path)  
                await txt.edit("Downloaded File")
                pdf = open(pdf_path,'rb')
                pdf_reader = PyPDF2.PdfFileReader(pdf) #pdfReaderObject
                await txt.edit("Getting Number of Pages....")
                num_of_pages = pdf_reader.getNumPages() # Number of Pages               
                await txt.edit(f"Found {num_of_pages} Page")
                page_no = pdf_reader.getPage(0) # pageObject
                await txt.edit("Finding Text from Pdf File... ")
                page_content = """ """ # EmptyString   
                chat_id = message.chat.id
                with open(f'{message.chat.id}.txt', 'a+') as text_path:   
                  for page in range (0,num_of_pages):              
                      page_no = pdf_reader.getPage(page) # Iteration of page number
                      page_content += page_no.extractText()
                await txt.edit(f"Creating Your Audio Book...\n Please Don't Do Anything")
                output_text = page_content + Thanks
              # Change Voice by editing the Language
                language = 'en-my'  # 'en': ['en-us', 'en-ca', 'en-uk', 'en-gb', 'en-au', 'en-gh', 'en-in',
                                    # 'en-ie', 'en-nz', 'en-ng', 'en-ph', 'en-za', 'en-tz'],
                tts_file = gTTS(text=output_text, lang=language, slow=False) 
                tts_file.save(f"{message.chat.id}.mp3")      
                with open(f"{message.chat.id}.mp3", "rb") as speech:
                      await bot.send_voice(chat_id, speech)   
                await txt.edit("Thanks For Using Me")    
                os.remove(pdf_path)  
                
                
           else :
                await message.reply("Please Reply to PDF file")
 except Exception as error :
           print(error)
           await txt.delete()
           os.remove(pdf_path)
		
		
		
		





