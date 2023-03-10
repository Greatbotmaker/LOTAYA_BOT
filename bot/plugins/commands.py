import os
import math
import re
import asyncio
import random
import logging, os, math
from info import PICS, PICS2, AUTO_FILTER_TXT, OWNER_LINK, M_LINK
from info import info
from os import environ
from bot import Bot

from gutils import extract_user, get_file_id, get_poster, last_online
from pyrogram.errors.exceptions.bad_request_400 import UserNotParticipant, MediaEmpty, PhotoInvalidDimensions, WebpageMediaEmpty
from pyrogram import Client, filters, enums, errors, types
from datetime import datetime
from pytz import timezone
from ..config import Config
from ..database import a_filter, usersDB
from ..utils.botTools import check_fsub, format_buttons, get_size, unpack_new_file_id, FORCE_TEXT
from ..utils.cache import Cache
from ..utils.imdbHelpers import get_poster
from ..utils.logger import LOGGER
from ..utils.decorators import is_banned
from pyrogram import Client, filters
from ..config import Config
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

TIMEZONE = (os.environ.get("TIMEZONE", "Asia/Yangon"))

log = LOGGER(__name__)
logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)

curr = datetime.now(timezone(TIMEZONE))
date = curr.strftime('%d %B, %Y')
time = curr.strftime('%I:%M:%S %p')






START_TEXT = """Hey {mention} π

I'm an advanced Auto filter bot with many capabilities!
There is no practical limits for my filtering capacity.

Only admin can access me π

- - - - - - - - - - - - - - -
For your bot editing
Contact :- @KOPAINGLAY15
- - - - - - - - - - - - - - -

**π²ππ΄π°ππΎπ :- <a href=https://t.me/KOPAINGLAY15>Mr.PAING LAY</a>**

**Join Group :- <a href=https://t.me/Movie_Group_MMSUB> My Group</a>** """


HELP_TEXT = """ FEAUTURES

β― For your bot editing
  Contact :- @KOPAINGLAY15

β― Modified By @KOPAINGLAY15 π

β― Special Courtesy To :
   β SUBINP
   β 
      
β― Bot Managed By :
   β @KOPAINGLAY15
   β @PAINGLAY15
   β               """


@Bot.on_message(filters.command("start") & filters.incoming)  # type: ignore
@is_banned
async def start_handler(bot: Bot, msg: types.Message):
    if len(msg.command) > 1:
        _, cmd = msg.command
        if cmd.startswith("filter"):
            if not await check_fsub(bot, msg, cmd):
                return
            key = cmd.replace("filter", "").strip()
            keyword = Cache.BUTTONS.get(key)
            filter_data = Cache.SEARCH_DATA.get(key)
            if not (keyword and filter_data):
                return await msg.reply("Search Expired\nPlease send movie name again.\n\nααΎα¬αα½α±ααΎα― αααΊαααΊαΈαα―ααΊαα½α¬αΈαα«ααΌα?α\nαα»α±αΈαα°αΈααΌα―α αα―ααΊααΎααΊα‘αααΊαα­α― \nGroup αα²βαα½ααΊ αααΊααΆαα±αΈαα­α―α·αα«α\n\n**@Movie_Zone_KP** ")
            files, offset, total_results, imdb, g_settings = filter_data

            settings = g_settings

            if settings["PM_IMDB"] and not g_settings["IMDB"]:
                imdb = await get_poster(keyword, file=(files[0])["file_name"])

            sts = await msg.reply("Please Wait...\n\nαααα±α¬αα·αΊαα«α....", quote=True)
            btn = await format_buttons(files, settings["CHANNEL"])
            if offset != "":
                req = msg.from_user.id if msg.from_user else 0
                btn.append(
                    [
                        types.InlineKeyboardButton(
                            text=f"π° 1/{math.ceil(int(total_results) / 10)} π°", callback_data="pages"
                        ),
                        types.InlineKeyboardButton(
                            text="NEXT β©", callback_data=f"next_{req}_{key}_{offset}"
                        ),
                    ]
                )
                
                
            else:
               
                btn.append([types.InlineKeyboardButton(text="ππ ππππ πππππ πππππππππ",callback_data="pages")])
                    
            if imdb:
                cap = Config.TEMPLATE.format(  # type: ignore
                    query=keyword,
                    **imdb,
                    **locals(),
                )

            else:
                cap = f"Hello Sir\n\nαα­ααΊβαα½α±ααΎα¬αα¬ {keyword} αα­α―αααΊαααΊααΎα¬αα½α±αα¬αα±αΈααΌαα¬αΈαα«αααΊα\n\nπ Request Dα΄α΄α΄ : <code>{date}</code>\nβ° Request TΙͺα΄α΄ : <code>{time}</code> - <code>{TIMEZONE}</code>\n\n</b><a href='https://t.me/Movie_Zone_KP/3'>Β© MKS & KP Channel</a>"
            if imdb and imdb.get("poster") and settings["PM_IMDB_POSTER"]:
                try:
                    await msg.reply_photo(
                        photo=imdb.get("poster"),  # type: ignore
                        caption=cap[:1024],
                        reply_markup=types.InlineKeyboardMarkup(btn),
                        quote=True,
                    )
                except (errors.MediaEmpty, errors.PhotoInvalidDimensions, errors.WebpageMediaEmpty):
                    pic = imdb.get("poster")
                    poster = pic.replace(".jpg", "._V1_UX360.jpg")
                    await msg.reply_photo(
                        photo=poster,
                        caption=cap[:1024],
                        reply_markup=types.InlineKeyboardMarkup(btn),
                        quote=True,
                    )
                except Exception as e:
                    log.exception(e)
                    await msg.reply_text(
                        cap, reply_markup=types.InlineKeyboardMarkup(btn), quote=True
                    )
            else:
                await msg.reply_photo(photo=random.choice(PICS2),
                    caption=cap,
                    reply_markup=types.InlineKeyboardMarkup(btn),
                    quote=True)                
                
            await sts.delete()
            return
        elif cmd.startswith("fsub"):
            invite_link = await bot.create_chat_invite_link(Config.FORCE_SUB_CHANNEL)
            btn = [
                [types.InlineKeyboardButton("Join Channel", url=invite_link.invite_link)],
            ]
            
            await msg.reply(FORCE_TEXT, reply_markup=types.InlineKeyboardMarkup(btn))

            
    
        
      
        
    m=await msg.reply_sticker("CAACAgQAAxkBAAIJSGOV6sHAHs148yj9qga-EyzXn6fdAAIMDQACX16QUOWPT2zBlmi9HgQ")    
    await asyncio.sleep(2)          
    await m.delete()
    await msg.reply_photo(
        photo=random.choice(PICS),
        caption=START_TEXT.format(mention=msg.from_user.mention),       
        reply_markup=types.InlineKeyboardMarkup(
            [                
                [
                    types.InlineKeyboardButton(
                        "β»οΈ πππβ ππβ πΎβππβ ππ πππΌ ππΌ β»οΈ", url="https://t.me/Movie_Group_MMSUB"
                    )
                ],
                [
                    types.InlineKeyboardButton( "ππ ππ ππ‘πππ₯π βππππππ", url='https://t.me/+4DDoxav12EwyYzA1')
                  
                ],
                [
                    types.InlineKeyboardButton('ππ βππππππ', callback_data="allchannel"),
                    types.InlineKeyboardButton('ππͺ πΎπ£π π¦π‘', callback_data="allgroups")                    
                ],
                [
                    types.InlineKeyboardButton('ππβ πππ£πππ€ πππ€π₯ ',  callback_data="vip"),
                    types.InlineKeyboardButton("π½πππ₯π¦π£ππ€", callback_data="help_data")                                                            
                ],
                [
                    types.InlineKeyboardButton("πΈπΉπππ", callback_data="about"),
                    types.InlineKeyboardButton("π»π πππ₯π", callback_data="donate")                    
                ],  
                [
                    types.InlineKeyboardButton("π»πΌππ", callback_data="DEVS"), 
                    types.InlineKeyboardButton(" πΉπ π₯ ππ¨πππ£  ", callback_data="owner")
                ]             
            ]
        )
    )


@Bot.on_callback_query(filters.regex("help"))  # type: ignore
async def help_handler_query(bot: Bot, query: types.CallbackQuery):
    await query.answer()
    await query.edit_message_text(
        HELP_TEXT,
        reply_markup=types.InlineKeyboardMarkup(
            [[
            types.InlineKeyboardButton('π πππππ ππππ π', callback_data='extra'),            
            ],[
            types.InlineKeyboardButton('πππππππ πππππππ', callback_data='gfilter'),
            types.InlineKeyboardButton('πππππ πππππππ', callback_data='autofilter')            
            ],[                       
            types.InlineKeyboardButton('β€οΈπππππππππ β€οΈ', callback_data='tele'),
            types.InlineKeyboardButton('π§‘ππππ-ππππππ§‘', callback_data='newdata')
            ],[         
            types.InlineKeyboardButton('π πππ π', callback_data='ttss'),           
            types.InlineKeyboardButton('π πππππ π', callback_data='purges')
            ],[
            types.InlineKeyboardButton('π€ππ_ππππππ€', callback_data='ytvid'),            
            types.InlineKeyboardButton('π€ππ_πππππ€', callback_data='ytsong')                                   
            ],[
            types.InlineKeyboardButton('π€ ππππ π€', callback_data='book'),
            types.InlineKeyboardButton('π ππππ π', callback_data='fond')            
            ],[
            types.InlineKeyboardButton('ππππππ πππππππππ', callback_data='gtrans'),
            types.InlineKeyboardButton('  πππππππ ', callback_data='coct')             
            ],[
            types.InlineKeyboardButton('π? ππππππ π?', callback_data='status'), 
            types.InlineKeyboardButton("βοΈ ππππ", callback_data="back")         
            ] ]        
           
        ),
    )
   

  
@Bot.on_callback_query(filters.regex("back"))  # type: ignore
async def home_handler(bot: Bot, query: types.CallbackQuery):
    await query.answer()
    await query.edit_message_text(
        START_TEXT.format(mention=query.from_user.mention),
        reply_markup=types.InlineKeyboardMarkup(
            [                
                [
                    types.InlineKeyboardButton(
                        "β»οΈ πππβ ππβ πΎβππβ ππ πππΌ ππΌ β»οΈ", url="https://t.me/Movie_Group_MMSUB"
                    )
                ],
                [
                    types.InlineKeyboardButton( "ππ ππ ππ‘πππ₯π βππππππ", url='https://t.me/+4DDoxav12EwyYzA1')
                  
                ],
                [
                    types.InlineKeyboardButton('ππ βππππππ', callback_data="allchannel"),
                    types.InlineKeyboardButton('ππͺ πΎπ£π π¦π‘', callback_data="allgroups")                    
                ],
                [
                    types.InlineKeyboardButton('ππβ πππ£πππ€ πππ€π₯ ',  callback_data="vip"),
                    types.InlineKeyboardButton("π½πππ₯π¦π£ππ€", callback_data="help_data")                                                            
                ],
                [
                    types.InlineKeyboardButton("πΈπΉπππ", callback_data="about"),
                    types.InlineKeyboardButton("π»π πππ₯π", callback_data="donate")                    
                ],  
                [
                    types.InlineKeyboardButton("π»πΌππ", callback_data="DEVS"), 
                    types.InlineKeyboardButton(" πΉπ π₯ ππ¨πππ£  ", callback_data="owner")
                ]               
            ]         
        ),
        disable_web_page_preview=True,      
   )
   
   
@Bot.on_message(filters.command("help") & filters.incoming)  # type: ignore
async def help_handler(bot: Bot, msg: types.Message):
     await msg.reply(HELP_TEXT,        
        reply_markup=types.InlineKeyboardMarkup(
            [[
            types.InlineKeyboardButton('π πππππ ππππ π', callback_data='extra'),            
            ],[
            types.InlineKeyboardButton('πππππππ πππππππ', callback_data='gfilter'),
            types.InlineKeyboardButton('πππππ πππππππ', callback_data='autofilter')            
            ],[                       
            types.InlineKeyboardButton('β€οΈπππππππππ β€οΈ', callback_data='tele'),
            types.InlineKeyboardButton('π§‘ππππ-ππππππ§‘', callback_data='newdata')
            ],[         
            types.InlineKeyboardButton('π πππ π', callback_data='ttss'),           
            types.InlineKeyboardButton('π πππππ π', callback_data='purges')
            ],[
            types.InlineKeyboardButton('π€ππ_ππππππ€', callback_data='ytvid'),            
            types.InlineKeyboardButton('π€ππ_πππππ€', callback_data='ytsong')                                   
            ],[
            types.InlineKeyboardButton('π€ ππππ π€', callback_data='book'),
            types.InlineKeyboardButton('π ππππ π', callback_data='fond')            
            ],[
            types.InlineKeyboardButton('ππππππ πππππππππ', callback_data='gtrans'),
            types.InlineKeyboardButton('  πππππππ ', callback_data='coct')             
            ],[
            types.InlineKeyboardButton('π? ππππππ π?', callback_data='status'), 
            types.InlineKeyboardButton("βοΈ ππππ", callback_data="back")         
            ] ]    
                  
       ),      
    )

      
@Bot.on_message(filters.command("stats"))  # type: ignore
async def get_stats(_, msg: types.Message):
    count = await a_filter.col.count_documents({})  # type: ignore
    size = (await a_filter.db.command("dbstats"))["dataSize"]  # type: ignore
    users = await usersDB.total_users_count()
    chats = await usersDB.total_chat_count() 
    monsize = await usersDB.get_db_size()
    free = 536870912 - monsize
    monsize = get_size(monsize)
    free = get_size(free)
    free = 536870912 - size
    await msg.reply(
        f"**Stats**\n\n**Total Files**: `{count}`"
        f"\n**Total Users**: {users}"
        f"\n**Total Chat** : {chats}"
        f"\n**Total DB Used:** `{get_size(size)}`"
        f"\n**Free:** `{get_size(free)}`"
        f"\n**Total   ** : {monsize} "
        f"\n**Free  ** : {free}"
    )
   

         
@Bot.on_message(filters.command("delete") & filters.user(Config.ADMINS))  # type: ignore
async def handleDelete(bot: Bot, msg: types.Message):
    """Delete file from database"""
    reply = msg.reply_to_message
    if reply and reply.media:
        msg = await msg.reply("Processing...β³", quote=True)
    else:
        await msg.reply("Reply to file with /delete which you want to delete", quote=True)
        return

    for file_type in ("document", "video", "audio"):
        media = getattr(reply, file_type, None)
        if media is not None:
            break
    else:
        await msg.edit("This is not supported file format")
        return

    file_id, file_ref = unpack_new_file_id(media.file_id)

    result = await a_filter.col.delete_one(
        {
            "_id": file_id,
        }
    )  # type: ignore
    if result.deleted_count:
        await msg.edit("File is successfully deleted from database")
    else:
        file_name = re.sub(r"(_|\-|\.|\+)", " ", str(media.file_name))
        result = await a_filter.col.delete_many(
            {"file_name": file_name, "file_size": media.file_size, "mime_type": media.mime_type}
        )  # type: ignore
        if result.deleted_count:
            await msg.edit("File is successfully deleted from database")
        else:
            await msg.edit("File not found in database")
            
            
@Bot.on_callback_query(filters.regex("vip"))  # type: ignore  
async def vip_home_handler(bot: Bot, query: types.CallbackQuery):
        buttons = [[
                    types.InlineKeyboardButton('π  VIP English Series π ', url='https://t.me/Serieslists'),
                    types.InlineKeyboardButton('π  VIP Chinese Seriesπ ', url='https://t.me/Chinese_Series_MCS')
                ],
                [
                    types.InlineKeyboardButton('π  VIP Thai Seriesπ ', url='https://t.me/ThaiSeries_MTS'),
                    types.InlineKeyboardButton('π  VIP Bollywood Seriesπ ', url='https://t.me/+1-VidI6DzaA0MDA1')
                ],
                [
                    types.InlineKeyboardButton('π  VIP Anime Seriesπ ', url='https://t.me/Anime_Animation_Series'),
                    types.InlineKeyboardButton('π  Korean Seriesπ ', url='https://t.me/MKSVIPLINK')
                ],
                [
                    types.InlineKeyboardButton("ππ βππππππ", callback_data="allchannel"),
                    types.InlineKeyboardButton("ππͺ πΎπ£π π¦π‘", callback_data="allgroups")                               
                ],[
                    types.InlineKeyboardButton("πππ πππ«π’ππ¬ πππ¦πππ«αααΊαααΊ", url="https://t.me/Kpautoreply_bot"),
                    types.InlineKeyboardButton("βοΈ πΉππΈβπ", callback_data="back") 
                ]]
        reply_markup = types.InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=info.VIP_TEXT,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )

@Bot.on_callback_query(filters.regex("status"))  # type: ignore  
async def status_home_handler(bot: Bot, query: types.CallbackQuery):
        buttons = [[
            types.InlineKeyboardButton('π±π°π²πΊ', callback_data='help')            
        ]]
        count = await a_filter.col.count_documents({})  # type: ignore
        size = (await a_filter.db.command("dbstats"))["dataSize"]  # type: ignore
        users = await usersDB.total_users_count()
        chats = await usersDB.total_chat_count() 
        monsize = await usersDB.get_db_size()
        free = 536870912 - monsize
        monsize = get_size(monsize)
        free = get_size(free)
        free = 536870912 - size
        reply_markup = types.InlineKeyboardMarkup(buttons) 
        await query.message.edit_text(
            text=info.STATUS_TXT.format(count, users, chats, get_size(size), get_size(free), monsize, free),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        ) 


@Bot.on_callback_query(filters.regex("owner"))  # type: ignore  
async def owner_home_handler(bot: Bot, query: types.CallbackQuery):
        buttons= [[
            types.InlineKeyboardButton('β£οΈ FOUNDER β£οΈ', url=OWNER_LINK),
            types.InlineKeyboardButton("MODERATORS", url=M_LINK)
            ],[
            types.InlineKeyboardButton("βοΈ πΉππΈβπ", callback_data="back")
        ]]
        reply_markup =types.InlineKeyboardMarkup(buttons)        
        await query.message.edit_text(
            text=info.OWNER_TXT,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
      
@Bot.on_callback_query(filters.regex("about"))  # type: ignore  
async def about_home_handler(bot: Bot, query: types.CallbackQuery):
        buttons= [[
            types.InlineKeyboardButton('β£οΈ ππΎπππ²π΄ π²πΎπ³π΄ β£οΈ', callback_data='source'),
            types.InlineKeyboardButton("βπΌπβ", callback_data="DEVS")
            ],[
            types.InlineKeyboardButton("βοΈ πΉππΈβπ", callback_data="back")
        ]]
        reply_markup =types.InlineKeyboardMarkup(buttons)        
        await query.message.edit_text(
            text=info.ABOUT_TXT,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )

@Bot.on_callback_query(filters.regex("source"))  # type: ignore  
async def source_home_handler(bot: Bot, query: types.CallbackQuery):
        buttons = [[
            types.InlineKeyboardButton('ππΎπππ²π΄ π²πΎπ³π΄', url='https://t.me/kopainglay15')
            ],[
            types.InlineKeyboardButton("βοΈ πΉππΈβπ", callback_data="about"),
            types.InlineKeyboardButton("βπππΌ", callback_data="back")
        ]]
        reply_markup = types.InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=info.SOURCE_TXT,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
         
         
@Bot.on_callback_query(filters.regex("DEVS"))  # type: ignore  
async def DEVS_home_handler(bot: Bot, query: types.CallbackQuery):
        buttons = [[
            types.InlineKeyboardButton("βοΈ πΉππΈβπ", callback_data="about"),
            types.InlineKeyboardButton('βπππΌ', callback_data="back")            
        ]]
        reply_markup = types.InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=info.DEVS_TEXT,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
      
@Bot.on_callback_query(filters.regex("allchannel"))  # type: ignore  
async def allchannel_home_handler(bot: Bot, query: types.CallbackQuery):
        buttons = [[
            types.InlineKeyboardButton("ππͺ πΎπ£π π¦π‘", callback_data="allgroups"),
            types.InlineKeyboardButton("ππΌβππΌπ ππππ", callback_data="vip")],[
            types.InlineKeyboardButton("βοΈ πΉππΈβπ", callback_data="back")
        ]]
        reply_markup = types.InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=info.ALL_CHANNEL,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
      
@Bot.on_callback_query(filters.regex("allgroups"))  # type: ignore  
async def allgroups_home_handler(bot: Bot, query: types.CallbackQuery):
        buttons = [[
            types.InlineKeyboardButton("ππ βππππππ", callback_data="allchannel"),
            types.InlineKeyboardButton("ππΌβππΌπ ππππ", callback_data="vip")],[
            types.InlineKeyboardButton("βοΈ πΉππΈβπ", callback_data="back")
        ]]
        reply_markup = types.InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=info.ALL_GROUPS,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
      
@Bot.on_callback_query(filters.regex("donate"))  # type: ignore  
async def donate_home_handler(bot: Bot, query: types.CallbackQuery):
        buttons = [[
            types.InlineKeyboardButton("βοΈ πΉππΈβπ", callback_data="back")         
        ]]
        reply_markup = types.InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=info.DONATE,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
 
      
@Bot.on_callback_query(filters.regex("autofilter"))  # type: ignore  
async def autofilter_home_handler(bot: Bot, query: types.CallbackQuery):
        buttons = [[
            types.InlineKeyboardButton("βοΈ πΉππΈβπ", callback_data="back")          
        ]]
        reply_markup = types.InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=info.AUTO_FILTER_TXT,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
      
@Bot.on_callback_query(filters.regex("extra"))  # type: ignore
async def extra_handler_query(bot: Bot, query: types.CallbackQuery):      
        buttons = [[
            types.InlineKeyboardButton('βοΈ π°π³πΌπΈπ½ πΎπ½π»π βοΈ', callback_data='admin')
            ],[
            types.InlineKeyboardButton('π π±π°π²πΊ', callback_data='help'),
        ]]
        reply_markup = types.InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=info.EXTRAMOD_TXT,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )   
      
@Bot.on_callback_query(filters.regex("gfilter"))  # type: ignore
async def gfilter_handler_query(bot: Bot, query: types.CallbackQuery):      
        buttons = [[
            types.InlineKeyboardButton('βοΈ πΉππΈβπ', callback_data='help'),
            types.InlineKeyboardButton('π±ππππΎπ½π', callback_data='button')
        ]]
        reply_markup = types.InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=info.MANUELFILTER_TXT,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
      
@Bot.on_callback_query(filters.regex("gtrans"))  # type: ignore
async def gtrars_handler_query(bot: Bot, query: types.CallbackQuery):      
        buttons = [[
            types.InlineKeyboardButton('βοΈ πΉππΈβπ', callback_data='help')
            
        ]]
        reply_markup = types.InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=info.GTRANS_TXT,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )      
      
@Bot.on_callback_query(filters.regex("button"))  # type: ignore
async def button_handler_query(bot: Bot, query: types.CallbackQuery):     
        buttons = [[
            types.InlineKeyboardButton('βοΈ πΉππΈβπ', callback_data='gfilter')
        ]]
        reply_markup = types.InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=info.BUTTON_TXT,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
      
      
@Bot.on_callback_query(filters.regex("coct"))  # type: ignore
async def coct_handler_query(bot: Bot, query: types.CallbackQuery): 
        buttons = [[
            types.InlineKeyboardButton('βοΈ πΉππΈβπ', callback_data='help')
        ]]
        reply_markup = types.InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=info.CONNECTION_TXT,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )        

@Bot.on_callback_query(filters.regex("tele"))  # type: ignore
async def tele_handler_query(bot: Bot, query: types.CallbackQuery):         
        buttons = [[
            types.InlineKeyboardButton('βοΈ πΉππΈβπ', callback_data='help')
        ]]
        reply_markup = types.InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=info.TELE_TXT,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        ) 
      
@Bot.on_callback_query(filters.regex("extra"))  # type: ignore
async def extra_handler_query(bot: Bot, query: types.CallbackQuery):      
        buttons = [[
            types.InlineKeyboardButton('βοΈ π°π³πΌπΈπ½ πΎπ½π»π βοΈ', callback_data='admin')
            ],[
            types.InlineKeyboardButton('π π±π°π²πΊ', callback_data='help_data'),
        ]]
        reply_markup = types.InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=info.EXTRAMOD_TXT,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
      
@Bot.on_callback_query(filters.regex("admin"))  # type: ignore
async def admin_handler_query(bot: Bot, query: types.CallbackQuery):   
        buttons = [[
            types.InlineKeyboardButton('πΆπ»πΎπ±π°π» π΅πΈπ»ππ΄π', callback_data='gfill'),
            types.InlineKeyboardButton('πππ΄π & π²π·π°π', callback_data='uschat')
            ],[
            types.InlineKeyboardButton('π π±π°π²πΊ', callback_data='extra')
        ]]
        reply_markup = types.InlineKeyboardMarkup(buttons)
        if query.from_user.id in Config.ADMINS:
            await query.message.edit_text(text=info.ADMIN_TXT, reply_markup=reply_markup, parse_mode=enums.ParseMode.HTML)
        else:
            await query.answer("Your Not Authorizer β οΈ", show_alert=True)   
            
            
@Bot.on_callback_query(filters.regex("gfill"))  # type: ignore
async def gfill_handler_query(bot: Bot, query: types.CallbackQuery): 
        buttons = [[            
            types.InlineKeyboardButton('π π±π°π²πΊ', callback_data='admin')
        ]]
        reply_markup = types.InlineKeyboardMarkup(buttons)        
        await query.message.edit_text(text=info.G_FIL_TXT, reply_markup=reply_markup, parse_mode=enums.ParseMode.HTML)
         
@Bot.on_callback_query(filters.regex("uschat"))  # type: ignore
async def uschat_handler_query(bot: Bot, query: types.CallbackQuery):         
        buttons = [[            
            types.InlineKeyboardButton('π π±π°π²πΊ', callback_data='admin')
        ]]
        reply_markup = types.InlineKeyboardMarkup(buttons)        
        await query.message.edit_text(text=info.US_CHAT_TXT, reply_markup=reply_markup, parse_mode=enums.ParseMode.HTML)
      
@Bot.on_callback_query(filters.regex("newdata"))  # type: ignore
async def newdata_handler_query(bot: Bot, query: types.CallbackQuery):          
        buttons = [[
            types.InlineKeyboardButton('βοΈ πΉππΈβπ', callback_data='help')
        ]]
        reply_markup = types.InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=info.FILE_TXT,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
      
@Bot.on_callback_query(filters.regex("ttss"))  # type: ignore
async def ttss_handler_query(bot: Bot, query: types.CallbackQuery):       
        buttons = [[
            types.InlineKeyboardButton('βοΈ πΉππΈβπ', callback_data='help')
        ]]
        reply_markup = types.InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=info.TTS_TXT,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )      
 
@Bot.on_callback_query(filters.regex("purges"))  # type: ignore
async def purges_handler_query(bot: Bot, query: types.CallbackQuery):       
        buttons = [[
            types.InlineKeyboardButton('βοΈ πΉππΈβπ', callback_data='help')
        ]]
        reply_markup = types.InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=info.PURGE_TXT,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )

@Bot.on_callback_query(filters.regex("ytvid"))  # type: ignore
async def ytvid_handler_query(bot: Bot, query: types.CallbackQuery):       
        buttons = [[
            types.InlineKeyboardButton('βοΈ πΉππΈβπ', callback_data='help')
        ]]
        reply_markup = types.InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=info.YT_VIDEO_TXT,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )


      
@Bot.on_callback_query(filters.regex("ytsong"))  # type: ignore
async def ytsong_handler_query(bot: Bot, query: types.CallbackQuery):  
        buttons = [[
            types.InlineKeyboardButton('βοΈ πΉππΈβπ', callback_data='help')
        ]]
        reply_markup = types.InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=info.YT_SONG_TXT,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )      
      
@Bot.on_callback_query(filters.regex("book"))  # type: ignore
async def book_handler_query(bot: Bot, query: types.CallbackQuery):      
        buttons = [[
            types.InlineKeyboardButton('βοΈ πΉππΈβπ', callback_data='help')
        ]]
        reply_markup = types.InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=info.BOOK_TXT,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
            
@Bot.on_callback_query(filters.regex("fond"))  # type: ignore
async def fond_handler_query(bot: Bot, query: types.CallbackQuery):          
        buttons = [[
            types.InlineKeyboardButton('βοΈ πΉππΈβπ', callback_data='help')
        ]]
        reply_markup = types.InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=info.FOND_TXT,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
               
      
      


            
            
  


