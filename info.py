import re
from os import environ

#start
PICS = (environ.get('PICS', 'https://telegra.ph/file/6bf69c30bd0dd7f5e390c.jpg https://telegra.ph/file/dbc8cd2ceca8d08976c52.jpg')).split()
PICS2 = (environ.get('PICS', 'https://telegra.ph/file/6bf69c30bd0dd7f5e390c.jpg https://telegra.ph/file/dbc8cd2ceca8d08976c52.jpg')).split()
OWNER_LINK = "https://t.me/KOPAINGLAY15"
M_LINK = "https://t.me/KPOWNER"

#Downloader
DOWNLOAD_LOCATION = environ.get("DOWNLOAD_LOCATION", "./DOWNLOADS/AudioBoT/")


AUTO_FILTER_TXT = "TEST"



class info(object): 
    
    BOOK_TXT = """β€ πππ₯π©: π ππ½πππ»πππ
    
πππ πππ πππππππ π πΏπ³π΅ ππππ ππ π πππππ ππππ π πππ ππππ πππππππ β―

β€ ππ¨π¦π¦ππ§ππ¬ ππ§π ππ¬ππ π:
βͺ /audiobook: π±πΎπππ ππππ πΌππππΊππ½ ππ πΊππ π―π£π₯ ππ ππΎππΎππΊππΎ πππΎ πΊππ½ππ"""



    ALL_CHANNEL = """ALL MOVIE LIST
    
π MOVIE ZONE π    
https://t.me/Movie_Zone_KP

πKP World Movie 1 π
https://t.me/+rYX-JDbH9MoxMDBl

πKP World Movie 2 π
https://t.me/joinchat/ISraAtYHjKQ4ODU1

πKP World Movie 3 π
https://t.me/joinchat/kWUmZootKSxhMDll

πKP World Movie 4 π
https://t.me/joinchat/5j1Z-515I_k2YWM1

πKP World Movie 5 π
https://t.me/+bB-NEPWIB5VhM2E1

πKp Cartoon Movie π
https://t.me/joinchat/WcNZvMdzkzc2NThl

π Movie By Artist Name π
https://t.me/+me4-0JmJkIplOGY1

πKP Adult Channelπ
https://t.me/+UuQm91WPBbU2NzA1


====================

Korean Series αα»α¬αΈααΌαα·αΊαααΊ

πMKS Main Channelπ
https://t.me/mksviplink

πMKS Main Channelπ
https://t.me/mksviplink2

πMKS All Drama Team π
https://t.me/joinchat/3xS_MTfvJSEzZjY1

πMKS Ongoing Channel π
https://t.me/ONGOING_MKS

====================

πKP World Movie List π
https://t.me/kpmovielist

- OWNER : - <a href=https://t.me/KOPAINGLAY15>Mr.PAING LAY</a>**"""

    
    
    ALL_GROUPS = """ALL GROUP LIST
    
π ααΌααΊαα¬αα¬αααΊαΈαα­α―αΈαα―ααΊααΎααΊ π
 https://t.me/Movie_Group_MMSUB
 
πKP Movie Request Group π
https://t.me/joinchat/_1Hs8V60HGs1NzA1

π Movie Zone  π
https://t.me/+e0fXraY_I743Mjk9

π Movie Zone BACKUP π
https://t.me/+e0fXraY_I743Mjk9
=================


π Request Group π 
https://t.me/MKS_RequestGroup

π Request Group 2 π 
https://t.me/+z5lhEpxP5Go4MWM1

- OWNER : - <a href=https://t.me/KOPAINGLAY15>Mr.PAING LAY</a>**"""



    
    VIP_TEXT  =  """VIP Series Info
    
Hello

 1. For the English Series, Lifetime will have to pay 3000 Kyats.
English Series List
https://t.me/Serieslists

 2. For the Thailand Series, Lifetime should pay only 3000 Kyats.
Thailand Series List
https://t.me/ThaiSeries_MTS

 3. For the Chinese Series, Lifetime should pay only 3000 Kyats.
Chinese Series List
https://t.me/Chinese_Series_MCS

 β­οΈ If you join the Package Membership for all 3 Series Channels, you will only pay 8000 Kyats from Lifetime.  (The population is limited.)


Take a screenshot of this Acc and send it. 

ππ» @KPOWNER"""
    
    DONATE = """Donate β¦οΈ 

Wave 
Acc Phone No -09404840521

KBZ Pay 
Acc Phone No -09404840521

AYA Pay 
Acc Phone No -09404840521


α‘ααΌαΆαα±αΈαα»ααΊαα»α¬αΈαα²α· α‘αααΊαααΌα±αα°αα»α¬αΈααΎα­αα«α  π @KPOWNERBOT"""
    
    DEVS_TEXT = """DEVS
    
β― Modified By @KOPAINGLAY15 π
    
For your bot editing
Contact :- @KOPAINGLAY15

β― Special Courtesy To :
   β Team Eva Maria
   β Team TrojanzHex
   β Team CrazyBotsz
   β Team InFoTel 
   β SUBINP
   
β― Bot Managed By :
   β @KOPAINGLAY15
   β @PAINGLAY15
   β               
 """
    
   
 
    GTRANS_TXT = """β€ πππ₯π©: π¦πππππΎ π³ππΊππππΊππΎπ
        
ππππ πππππππ πππππ π’ππ ππ πππππππππ π πππ‘π ππ πΊππ πππππππππ π’ππ π πππ. ππππ πππππππ π ππππ ππ ππππ ππ πππ πππππ β―

β€ ππ¨π¦π¦ππ§ππ¬ ππ§π ππ¬ππ π:
βͺ/tr - π³π πππΊππππΊππΎπ ππΎπππ ππ πΊ πππΎπΌππΏπΌ ππΊππππΊππΎ

β€ π­πππΎ:
πΆππππΎ πππππ /tr πππ ππππππ½ πππΎπΌππΏπ πππΎ ππΊππππΊππΎ πΌππ½πΎ
βπ€ππΊππππΎ: /ππ πy

β’ πΎπ = π€ππππππ
β’ my = Myanmar

π²ππ΄π°ππΎπ :- <a href=https://t.me/KOPAINGLAY15>Mr.PAING LAY</a>**"""
        
    
    OWNER_TXT = """<b>OWNER:</b>
    
- OWNER 1 : - <a href=https://t.me/KPOWNER>Mr.SITT</a>
- OWNER 2 : - <a href=https://t.me/KOPAINGLAY15>Mr.PAING LAY</a>**
- OWNER 3 : - <a href=https://t.me/MKSVIPLINK>MKS</a>**"""
    
    PURGE_TXT = """<b>Purge</b>
    
Delete A Lot Of Messages From Groups! 
    
 <b>ADMIN</b> 
β /purge :- Delete All Messages From The Replied To Message, To The Current Message

π²ππ΄π°ππΎπ :- <a href=https://t.me/KOPAINGLAY15>Mr.PAING LAY</a>**"""


    CREATOR_REQUIRED = """β<b>You have To Be The Group Creator To Do That.</b>"""
      
    INPUT_REQUIRED = "β **Arguments Required**"
      
    KICKED = """βοΈ Successfully Kicked {} Members According To The Arguments Provided."""
      
    START_KICK = """π? Removing Inactive Members This May Take A While..."""
      
    ADMIN_REQUIRED = """β<b>I will not go where I am not made Admin Bii..Add Me Again with all admin rights.</b>"""
      
    DKICK = """βοΈ Kicked {} Deleted Accounts Successfully."""
      
    FETCHING_INFO = """<b>Let's get rid of everything now...</b>"""
    
    
    OWNER_TEXT = """BOT OWNER
    
β― Modified By @KOPAINGLAY15 π
    
β― Special Courtesy To :
   β SUBINP
   β 
      
β― Bot Managed By :
   β @KOPAINGLAY15
   β @PAINGLAY15
   β               """
 
  

    ABOUT_TXT = """β― πΌπ π½π°πΌπ΄ :IS AUTO FILTER BOT
β― π²ππ΄π°ππΎπ :- <a href=https://t.me/KOPAINGLAY15>Mr.PAING LAY</a>**
β― π»πΈπ±ππ°ππ : πΏπππΎπΆππ°πΌ
β― π»π°π½πΆππ°πΆπ΄ : πΏπππ·πΎπ½ πΉ
β― π³π°ππ° π±π°ππ΄ : πΌπΎπ½πΆπΎ-π³π±
β― π±πΎπ ππ΄πππ΄π : π°π½πππ·π΄ππ΄
β― π±ππΈπ»π³ ππ΄πππΈπΎπ½: πΏππΎπ΅π΄πππΎπ-π±πΎπ π3.0.0"""

    SOURCE_TXT = """<b>NOTE:</b>
- ππΎπππ²π΄ π²πΎπ³π΄ π²π»πΈπ²πΊ π·π΄π π :- <a href=https://t.me/KOPAINGLAY15>Mr.PAING LAY</a>

<b>DEVS:</b>
- π³ππ 1 : - <a href=https://t.me/KPOWNER>Mr.SITT</a>
- π³ππ 2 : - <a href=https://t.me/KOPAINGLAY15>Mr.PAING LAY</a>**"""

    FILE_TXT = """β€ πππ₯π©: ππ’π₯π ππ­π¨π«π ππ¨ππ?π₯π../

<b>π±π πππΈπ½πΆ ππ·πΈπ πΌπΎπ³ππ»π΄ ππΎπ π²π°π½ πππΎππ΄ π΅πΈπ»π΄π πΈπ½ πΌπ π³π°ππ°π±π°ππ΄ π°π½π³ πΈ ππΈπ»π» πΆπΈππ΄ ππΎπ π° πΏπ΄ππΌπ°π½π΄π½π π»πΈπ½πΊ  ππΎ π°π²π²π΄ππ ππ·π΄ ππ°ππ΄π³ π΅πΈπ»π΄π.πΈπ΅ ππΎπ ππ°π½π ππΎ π°π³π³ π΅πΈπ»π΄π π΅ππΎπΌ π° πΏππ±π»πΈπ² π²π·π°π½π½π΄π» ππ΄π½π³ ππ·π΄ π΅πΈπ»π π»πΈπ½πΊ πΎπ½π»π  πΎπ ππΎπ ππ°π½π ππΎ π°π³π³ π΅πΈπ»π΄π π΅ππΎπΌ π°  πΏππΈππ°ππ΄ π²π·π°π½π½π΄π» ππΎπ πΌπππ πΌπ°πΊπ΄ πΌπ΄ π°π³πΌπΈπ½ πΎπ½ ππ·π΄ π²π·π°π½π½π΄π» ππΎ π°π²π²π΄ππ π΅πΈπ»π΄π...//</b>

βͺΌ ππ¨π¦π¦ππ§ππ¬ ππ§π ππ¬ππ π βΊ

βͺ /plink βΊβΊ <b>ππ΄πΏπ»π ππΎ π°π½π πΌπ΄π³πΈπ° ππΎ πΆπ΄π π»πΈπ½πΊ.</b>
βͺ /pbatch βΊβΊ <b>πππ΄ ππΎππ πΌπ΄π³πΈπ° π»πΈπ½πΊ ππΈππ· ππ·πΈπ π²πΎπΌπΌπ°π½π³.</b>
βͺ /batch βΊβΊ <b>ππΎ π²ππ΄π°ππ΄ π»πΈπ½πΊ π΅πΎπ πΌππ»ππΈπΏπ»π΄ π΅πΈπ»π΄π.</b>

βͺΌ ππ±ππ¦π©π₯π βΊ

<code>/batch https://t.me/MKSVIPLINK https://t.me/MKSVIPLINK/code>

π²ππ΄π³πΈππ :- <a href=https://t.me/KOPAINGLAY15>Mr.PAING LAY</a>**"""
    
    MANUELFILTER_TXT = """Help: <b>Filters</b>

- Filter is the feature were users can set automated replies for a particular keyword and α©αα©α­  will respond whenever a keyword is found the message

<b>NOTE:</b>
1. This bot should have admin privillage.
2. only admins can add filters in a chat.
3. alert buttons have a limit of 64 characters.

<b>Commands and Usage:</b>
β’ /filter - <code>add a filter in chat</code>
β’ /filters - <code>list all the filters of a chat</code>
β’ /del - <code>delete a specific filter in chat</code>
β’ /delall - <code>delete the whole filters in a chat (chat owner only)</code>

β’ <code>/g_filter off</code> use this commoand + on/off in your group to control global filter in your group"""
   
    BUTTON_TXT = """Help: <b>Buttons</b>

-this bot Supports both url and alert inline buttons.

<b>NOTE:</b>
1. Telegram will not allows you to send buttons without any content, so content is mandatory.
2. This bot supports buttons with any telegram media type.
3. Buttons should be properly parsed as markdown format

<b>URL buttons:</b>
<code>[Button Text](buttonurl:xxxxxxxxxxxx)</code>

<b>Alert buttons:</b>
<code>[Button Text](buttonalert:This is an alert message)</code>

π²ππ΄π³πΈππ :- <a href=https://t.me/KOPAINGLAY15>Mr.PAING LAY</a>**"""

    AUTO_FILTER_TXT = """**π°πππΎ π΅πΈπ»ππ΄π πΌπΎπ³ππ»π΄.. 

π°πππΎ π΅πΈπ»ππ΄π πΈπ ππ·π΄ π΅π΄π°ππππ΄ ππΎ π΅πΈπ»ππ΄π π°π½π³ ππ°ππ΄  ππ·π΄ π΅πΈπ»π΄π π°πππΎπΌπ°ππΈπ²π°π»π»π π΅ππΎπΌ π²π·π°π½π½π΄π» ππΎ πΆππΎππΏ.

π²ππ΄π³πΈππ :- <a href=https://t.me/KOPAINGLAY15>Mr.PAING LAY</a>**"""

    CONNECTION_TXT = """Help: <b>Connections</b>

- Used to connect bot to PM for managing filters 
- it helps to avoid spamming in groups.

<b>NOTE:</b>
1. Only admins can add a connection.
2. Send <code>/connect</code> for connecting me to ur PM

<b>Commands and Usage:</b>
β’ /connect  - <code>connect a particular chat to your PM</code>
β’ /disconnect  - <code>disconnect from a chat</code>
β’ /connections - <code>list all your connections</code>

π²ππ΄π³πΈππ :- <a href=https://t.me/KOPAINGLAY15>Mr.PAING LAY</a>**"""

    EXTRAMOD_TXT = """Help: <b>Extra Modules</b>

<b>NOTE:</b>
these are the extra features of this bot

<b>Commands and Usage:</b>
β’ /id - <code>get id of a specifed user.</code>
β’ /info  - <code>get information about a user.</code>
β’ /imdb  - <code>get the film information from IMDb source.</code>
β’ /search  - <code>get the film information from various sources.</code>"""

    ADMIN_TXT = """<b>Ι΄α΄α΄α΄:</b>
<code>TΚΙͺs Mα΄α΄α΄Κα΄ OΙ΄ΚΚ Wα΄Κα΄s Fα΄Κ MΚ Aα΄α΄ΙͺΙ΄s</code>

π <u><b>Basic Command</b></u>
β’ /logs - <code>α΄α΄ Ι’α΄α΄ α΄Κα΄ Κα΄α΄α΄Ι΄α΄ α΄ΚΚα΄Κκ±</code>
β’ /stats - <code>α΄α΄ Ι’α΄α΄ κ±α΄α΄α΄α΄κ± α΄κ° κ°ΙͺΚα΄κ± ΙͺΙ΄ α΄Κ.</code>

ποΈ <u><b>Database & Server Command</b></u>
β’ /status - <code>α΄α΄ Ι’α΄α΄ sα΄α΄α΄α΄s α΄? sα΄Κα΄ α΄Κ</code>
β’ /stats - <code>α΄α΄ Ι’α΄α΄ α΄α΄α΄α΄α΄Κα΄κ±α΄ κ±α΄α΄α΄α΄κ±</code>
β’ /delete - <code>α΄α΄ α΄α΄Κα΄α΄α΄ α΄ κ±α΄α΄α΄Ιͺκ°Ιͺα΄ κ°ΙͺΚα΄ κ°Κα΄α΄ α΄Κ.</code>
β’ /deleteall - <code>α΄α΄ α΄α΄Κα΄α΄α΄ α΄ΚΚ κ°ΙͺΚα΄s κ°Κα΄α΄ α΄Κ.</code>
β’ /users - <code>α΄α΄ Ι’α΄α΄ ΚΙͺκ±α΄ α΄κ° α΄Κ α΄κ±α΄Κκ± α΄Ι΄α΄ Ιͺα΄κ±.</code>
β’ /chats - <code>α΄α΄ Ι’α΄α΄ ΚΙͺκ±α΄ α΄κ° α΄Κ α΄Κα΄α΄κ± α΄Ι΄α΄ Ιͺα΄κ±</code>
β’ /channel - <code>α΄α΄ Ι’α΄α΄ ΚΙͺκ±α΄ α΄κ° α΄α΄α΄α΄Κ α΄α΄Ι΄Ι΄α΄α΄α΄α΄α΄ α΄Κα΄Ι΄Ι΄α΄Κκ±</code>"""

    US_CHAT_TXT = """<b>Ι΄α΄α΄α΄:</b>
<code>TΚΙͺs Mα΄α΄α΄Κα΄ OΙ΄ΚΚ Wα΄Κα΄s Fα΄Κ MΚ Aα΄α΄ΙͺΙ΄s</code>

π― <u><b>Chat & User</b></u>
β’ /broadcast - <code>α΄α΄ ΚΚα΄α΄α΄α΄α΄κ±α΄ α΄ α΄α΄κ±κ±α΄Ι’α΄ α΄α΄ α΄ΚΚ α΄κ±α΄Κκ±</code>
β’ /group_broadcast - <code>α΄α΄ ΚΚα΄α΄α΄α΄α΄sα΄ α΄ α΄α΄ssα΄Ι’α΄ α΄α΄ α΄ΚΚ α΄α΄Ι΄Ι΄α΄α΄α΄α΄α΄ Ι’Κα΄α΄α΄s</code>
β’ /leave  - <code>α΄α΄ Κα΄α΄α΄ α΄ κ°Κα΄α΄ α΄ α΄Κα΄α΄.</code>
β’ /disable  -  <code>α΄α΄ α΄Ιͺκ±α΄ΚΚα΄ α΄ α΄Κα΄α΄.</code>
β’ /invite - <code>Tα΄ Ι’α΄α΄ α΄Κα΄ ΙͺΙ΄α΄ Ιͺα΄α΄ ΚΙͺΙ΄α΄ α΄? α΄Ι΄Κ α΄Κα΄α΄ α΄‘Κα΄Κα΄ α΄Κα΄ Κα΄α΄ Ιͺs α΄α΄α΄ΙͺΙ΄.</code>
β’ /ban_user  - <code>α΄α΄ Κα΄Ι΄ α΄ α΄κ±α΄Κ.</code>
β’ /unban_user  - <code>α΄α΄ α΄Ι΄Κα΄Ι΄ α΄ α΄κ±α΄Κ.</code>
β’ /restart - <code>Tα΄ Rα΄sα΄α΄Κα΄ α΄ Bα΄α΄</code>
β’ /usend - <code>Tα΄ Sα΄Ι΄α΄ α΄ Mα΄ssΙ’α΄α΄ α΄α΄ Pα΄Κα΄Ιͺα΄α΄Κα΄Κ Usα΄Κ</code>
β’ /gsend - <code>Tα΄ Sα΄Ι΄α΄ α΄ Mα΄ssα΄Ι’α΄ α΄α΄ Pα΄Κα΄Ιͺα΄α΄Κα΄Κ CΚα΄α΄</code>"""

    G_FIL_TXT = """<b>Ι΄α΄α΄α΄:</b>
<code>TΚΙͺs Mα΄α΄α΄Κα΄ OΙ΄ΚΚ Wα΄Κα΄s Fα΄Κ MΚ Aα΄α΄ΙͺΙ΄s</code>

π₯ <u><b>Adv Global Filter </b></u>
β’ /gfilter - <code>α΄α΄ α΄α΄α΄ Ι’Κα΄Κα΄Κ ?ΙͺΚα΄α΄Κs</code>
β’ /gfilters - <code>α΄α΄ α΄ Ιͺα΄α΄‘ ΚΙͺsα΄ α΄? α΄ΚΚ Ι’Κα΄Κα΄Κ ?ΙͺΚα΄α΄Κs<code>
β’ /delg - <code>α΄α΄ α΄α΄Κα΄α΄α΄ α΄ sα΄α΄α΄Ιͺ?Ιͺα΄ Ι’Κα΄Κα΄Κ ?ΙͺΚα΄α΄Κ</code>
β’ /delallg - <code>α΄α΄ α΄α΄Κα΄α΄α΄ α΄ΚΚ Ι’Κα΄Κα΄Κ κ°ΙͺΚα΄α΄Κκ±</code>

π²ππ΄π³πΈππ :- <a href=https://t.me/KOPAINGLAY15>Mr.PAING LAY</a>**
"""

    STATUS_TXT = """<b>αβΊ ππΎππ°π» π΅πΈπ»π΄π: <code>{}</code></b>
<b>αβΊ ππΎππ°π» πππ΄ππ: <code>{}</code></b>
<b>αβΊ ππΎππ°π» π²π·π°ππ: <code>{}</code></b>
<b>αβΊ πππ΄π³ πππΎππ°πΆπ΄: <code>{}</code> πΌπ±</b>
<b>αβΊ π΅ππ΄π΄ πππΎππ°πΆπ΄: <code>{}</code> πΌπ±</b>
<b>αβΊ ππΎππ°π» : <code>{}</code> πΌπ±</b>
<b>αβΊ π΅ππ΄π΄ : <code>{}</code> πΌπ±</b>
"""
    LOG_TEXT_G = """#πππ°ππ«π¨π?π©
    
<b>αβΊ ππ«π¨π?π© βͺΌ {a}(<code>{b}</code>)</b>
<b>αβΊ π ππ βͺΌ @{c}
<b>αβΊ ππ¨π­ππ₯ πππ¦πππ«π¬ βͺΌ {d}</b>
<b>αβΊ πππππ ππ² βͺΌ {e}</b>

By {f}
"""
    LOG_TEXT_P = """#πππ°ππ¬ππ«
    
<b>αβΊ ππ - <code>{}</code></b>
<b>αβΊ πππ¦π - {}</b>
<b>αβΊ ππ - @{}</b>

By @{} """
   
    ZOMBIES_TXT = """π·π΄π»πΏ ππΎπ ππΎ πΊπΈπ²πΊ πππ΄ππ

<b>Kick incative members from group. Add me as admin with ban users permission in group.</b>

<b>Commands and Usage:</b>
β’ /inkick - command with required arguments and i will kick members from group.
β’ /instatus - to check current status of chat member from group.
β’ /inkick within_month long_time_ago - to kick users who are offline for more than 6-7 days.
β’ /inkick long_time_ago - to kick members who are offline for more than a month and Deleted Accounts.
β’ /dkick - to kick deleted accounts."""

    IMAGE_TXT = """β€ πππ₯π©: Iα΄α΄Ι’α΄

ππππ πππππππ πππππ π’ππ ππ ππππ πππππ ππππ’ ππππππ’ 

β€ ππ¨π¦π¦ππ§ππ¬ ππ§π ππ¬ππ π:

βͺ π©πππ ππΎππ½ ππΎ πΊ πππΊππΎ ππ πΎπ½ππ β¨

π¬πΊπ½πΎ π»π <a href=https://t.me/mr_MKN>Mr.MKN TG</a>"""

    RESTRIC_TXT = """β€ πππ₯π©: Mα΄α΄α΄ π«

πππππ πππ πππ ππππππππ π πππππ πππππ πππ πππ ππ ππππππ πππππ πππππ ππππ πππππππππππ’.

βͺ/ban: π³π π»πΊπ πΊ πππΎπ πΏπππ πππΎ πππππ.
βͺ/unban: π³π πππ»πΊπ πΊ πππΎπ ππ πππΎ πππππ.
βͺ/tban: π³π ππΎπππππΊππππ π»πΊπ πΊ πππΎπ.
βͺ/mute: π³π ππππΎ πΊ πππΎπ ππ πππΎ πππππ.
βͺ/unmute: π³π ππππππΎ πΊ πππΎπ ππ πππΎ πππππ.
βͺ/tmute: π³π ππΎπππππΊππππ ππππΎ πΊ πππΎπ.

β€ π­πππΎ:
πΆππππΎ πππππ /tmute ππ /tban πππ ππππππ½ πππΎπΌππΏπ πππΎ ππππΎ πππππ.

βπ€ππΊππππΎ: /ππ»πΊπ 2π½ ππ /πππππΎ 2π½.
πΈππ πΌπΊπ πππΎ ππΊπππΎπ: π/π/π½. 
 β’ π = ππππππΎπ
 β’ π = πππππ
 β’ π½ = π½πΊππ"""


    PIN_TXT ="""<b>PIN MODULE</b>
<b>πΏπΈπ½ π° πΌπ΄πππ°πΆπ΄../</b>

<b>π°π»π» ππ·π΄ πΏπΈπ½ ππ΄πΏπ»π°ππ΄π³ π²πΎπΌπΌπ°π½π³π π²π°π½ π±π΄ π΅πΎππ½π³ π·π΄ππ΄::</b>

<b>ππ²πΎπΌπΌπ°π½π³π π°π½π³ πππ°πΆπ΄π</b>

β /pin :- ππΎ πΏπΈπ½ ππ·π΄ πΌπ΄πππ°πΆπ΄ πΎπ½ ππΎππ π²π·π°ππ
β /unpin :- ππΎ ππ½πΏπΈπ½ ππ·π΄ π²ππππ΄π΄π½π πΏπΈπ½π½π΄π³ πΌπ΄ππ°π°πΆπ΄"""
    
    

    YT_VIDEO_TXT = """ π·π΄π»πΏ ππΎπ ππΎ π³πΎππ½π»πΎπ°π³ ππΈπ³π΄πΎ π΅ππΎπΌ ππΎππππ±π΄

β’ ππ΄π’π¨π¦
π π°πΆ ππ’π― ππ°πΈπ―π­π°π’π₯ ππ―πΊ ππͺπ₯π¦π° ππ³π°π? π π°πΆπ΅πΆπ£π¦

ππ€π¬ ππ€ ππ¨π
β’ ππΊπ±π¦ /video or /mp4 ππ―π₯ (https://youtu.be/kB9TkCs8cX0)
β’ ππΉπ’π?π±π­π¦:
<code>/mp4 https://youtu.be/kB9TkCs8cX0</code>
<code>/video https://youtu.be/kB9TkCs8cX0</code>

π²ππ΄π³πΈππ :- <a href=https://t.me/KOPAINGLAY15>Mr.PAING LAY</a>"""


    YT_SONG_TXT = """<b>ππΎπ½πΆ π³πΎππ½π»πΎπ°π³ πΌπΎπ³ππ»π΄</b>
    
<b>ππΎπ½πΆ π³πΎππ½π»πΎπ°π³ πΌπΎπ³ππ»π΄, π΅πΎπ ππ·πΎππ΄ ππ·πΎ π»πΎππ΄ πΌπππΈπ². ππΎπ π²π°π½ πππ΄ ππ·πΈπ π΅π΄π°πππ΄ π΅πΎπ π³πΎππ½π»πΎπ°π³ π°π½π ππΎπ½πΆ ππΈππ· πππΏπ΄π π΅π°ππ ππΏπ΄π΄π³.ππΎππΊπ πΎπ½π»π πΎπ½ πΆππΎππΏπ../</b>

<b>π²πΎπΌπΌπ°π½π³π</b>
βΊβΊ  /song ππΎπ½πΆ π½π°πΌπ΄

ππΎππΊπ πΎπ½π»π πΎπ½ πΆππΎππΏ

π²ππ΄π³πΈππ :- <a href=https://t.me/KOPAINGLAY15>Mr.PAING LAY</a>**"""

    TTS_TXT = """Help: <b> TTS π€ module:</b>

Translate text to speech

<b>Commands and Usage:</b>

β’ /tts <text> : convert text to speech

<b>NOTE:</b>

β’ IMDb should have admin privillage.
β’ These commands works on both pm and group.
β’ IMDb can translate texts to 200+ languages.

π²ππ΄π³πΈππ :- <a href=https://t.me/KOPAINGLAY15>Mr.PAING LAY</a>**"""

    PINGS_TXT ="""<b>π Ping:</b>

Helps you to know your ping πΆπΌββοΈ

<b>Commands:</b>

β’ /alive - To check you are alive.
β’ /ping - To get your ping.
<b>πΉUsageπΉ :</b>

β’ This commands can be used in pms and groups
β’ This commands can be used buy everyone in the groups and bots pm
β’ Share us for more features"""

    TELE_TXT = """<b>β«οΈHELP: TelegraphβͺοΈ</b>

Do as you wish with telegra.ph module!

</b>USAGE:</b>

π€§ /telegraph - Send me this command reply with Picture or Vide Under (5MB) 

<b>NOTE:</b>

β’ This Command Is Available in goups and pms
β’ This Command Can be used by everyone

π²ππ΄π³πΈππ :- <a href=https://t.me/KOPAINGLAY15>Mr.PAING LAY</a>**"""

    JSON_TXT ="""<b>JSON:</b>

Bot returns json for all replied messages with /json

<b>Features:</b>

Message Editting JSON
Pm Support
Group Support

<b>Note:</b>

Everyone can use this command , if spaming happens bot will automatically ban you from the group."""

   
      
    CARB_TXT = """βΎοΈππππ£ ππ’π₯ πππ₯ππ’π‘β½οΈ
π²π°ππ±πΎπ½ πΈπ π° π΅π΄πππππ΄ ππΎ πΌπ°πΊπ΄ ππ·π΄ πΈπΌπ°πΆπ΄ π°π ππ·πΎππ½ πΈπ½ ππ·π΄ ππΎπΏ ππΈππ· ππΎπππ΄ ππ΄πππ.
π΅πΎπ πππΈπ½πΆ ππ·π΄ πΌπΎπ³ππ»π΄ πΉπππ ππ΄π½π³ ππ·π΄ ππ΄ππ π°π½π³ ππ΄πΏπ»π ππΎ πΈπ ππΈππ· /carbon π²πΎπΌπΌπ°π½π³ ππ·π΄ π±πΎπ ππΈπ»π» ππ΄πΏπ»π ππΈππ· ππ·π΄ π²π°ππ±πΎπ½ πΈπΌπ°πΆπ΄"""

    FOND_TXT = """βΎοΈππππ£ ππ’π₯ ππ’π‘π§π¦β½οΈ
π΅πΎπ½π πΈπ π° πΌπΎπ³ππ»π΄ π΅πΎπ πΌπ°πΊπ΄ ππΎππ ππ΄ππ ππππ»πΈππ·.
π΅πΎπ πππ΄ ππ·π°π π΅π΄πππππ΄ πππΏπ΄ /font <your text> ππ·π΄π½ ππΎππ ππ΄ππ πΈπ ππ΄π°π³π."""

    SHARE_TXT = """βΎοΈππππ£ ππ’π₯ π¦πππ₯π π§ππ«π§β½οΈ

β€ ππ¨π¦π¦ππ§ππ¬ ππ§π ππ¬ππ π:
β’ /share - πππππ’ ππππ π°ππ’ πππ‘π ππ ππππ ππππ π²ππππππ """

    FILE_STORE_CHANNEL = 'FILE_STORE_CHANNEL'

    MELCOW_NEW_USERS = ((('MELCOW_NEW_USERS', "True")), True)

    PROTECT_CONTENT =((('PROTECT_CONTENT', "False")), False)

    PUBLIC_FILE_STORE = ((('PUBLIC_FILE_STORE', "True")), True)

    


    


