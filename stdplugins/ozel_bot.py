import asyncio
import datetime
import logging
from telethon import events
from telethon.tl import functions, types

from sample_config import Config

logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING)
logger = logging.getLogger(__name__)



@borg.on(events.NewMessage(func=lambda e: e.is_group))
async def oto(event):
    my_id = await event.client.get_me()
    
    mesaj = event.message.message
    # if not my_id.id:
    if mesaj == ("selam") and not event.message.from_id == my_id.id:
        await event.reply("selammm")
    elif mesaj == ("Selam") and not event.message.from_id == my_id.id:
        await event.reply("selamm")
    elif mesaj == ("Sea") and not event.message.from_id == my_id.id:
        await event.reply("ase")
    elif mesaj == ("sea") and not event.message.from_id == my_id.id:
        await event.reply("ase")
    elif mesaj == ("sa") and not event.message.from_id == my_id.id:
        await event.reply("ase")
    elif mesaj == ("Sa") and not event.message.from_id == my_id.id:
        await event.reply("ase")
    elif mesaj == ("SA") and not event.message.from_id == my_id.id:
        await event.reply("ase")
    elif mesaj == ("Slm") and not event.message.from_id == my_id.id:
        await event.reply("slm")
    elif mesaj == ("slm") and not event.message.from_id == my_id.id:
        await event.reply("slm")
    elif mesaj == ("Selamun aleyküm") and not event.message.from_id == my_id.id:
        await event.reply("aleyküm selam")
    elif mesaj == ("Selamun Aleyküm") and not event.message.from_id == my_id.id:
        await event.reply("aleyküm selam")
    elif mesaj == ("selamun aleyküm") and not event.message.from_id == my_id.id:
        await event.reply("aleyküm selam")

    elif mesaj == ("naber") and not event.message.from_id == my_id.id:
        await event.reply("iyidir senden naber")
    elif mesaj == ("Naber") and not event.message.from_id == my_id.id:
        await event.reply("iyidir senden naber")
    elif mesaj == ("nbr") and not event.message.from_id == my_id.id:
        await event.reply("iyidir senden naber")
    elif mesaj == ("Nbr") and not event.message.from_id == my_id.id:
        await event.reply("iyidir senden naber")
    elif mesaj == ("NBR") and not event.message.from_id == my_id.id:
        await event.reply("iyidir senden naber")
    elif mesaj == ("Nasılsın") and not event.message.from_id == my_id.id:
        await event.reply("iyiyim sen nasılsın")
    elif mesaj == ("nasılsın") and not event.message.from_id == my_id.id:
        await event.reply("iyiyim sen nasılsın")

    elif mesaj == ("napıyon") and not event.message.from_id == my_id.id:
        await event.reply("oturuyom sen")
    elif mesaj == ("Napıyon") and not event.message.from_id == my_id.id:
        await event.reply("oturuyom sen")
    elif mesaj == ("ne yapıyorsun") and not event.message.from_id == my_id.id:
        await event.reply("oturuyom sen")
    elif mesaj == ("napıyorsun") and not event.message.from_id == my_id.id:
        await event.reply("oturuyom sen")
    elif mesaj == ("Napıyonuz") and not event.message.from_id == my_id.id:
        await event.reply("oturuyom sen")
    elif mesaj == ("Napiyosunuz") and not event.message.from_id == my_id.id:
        await event.reply("oturuyom sen")

    elif mesaj == ("Günaydın") and not event.message.from_id == my_id.id:
        await event.reply("Sanada günaydın")
    elif mesaj == ("Gunaydın") and not event.message.from_id == my_id.id:
        await event.reply("Sanada günaydın")
    elif mesaj == ("günaydın") and not event.message.from_id == my_id.id:
        await event.reply("Sanada günaydın")
    elif mesaj == ("gunaydın") and not event.message.from_id == my_id.id:
        await event.reply("Sanada günaydın")

    elif mesaj == ("İyi geceler") and not event.message.from_id == my_id.id:
        await event.reply("Sanada iyi geceler")
    elif mesaj == ("iyi geceler") and not event.message.from_id == my_id.id:
        await event.reply("Sanada iyi geceler")
    elif mesaj == ("İyi Geceler") and not event.message.from_id == my_id.id:
        await event.reply("Sanada iyi geceler")
    elif mesaj == ("ıyı geceler") and not event.message.from_id == my_id.id:
        await event.reply("Sanada iyi geceler")
    elif mesaj == ("İYİ GECELER") and not event.message.from_id == my_id.id:
        await event.reply("Sanada iyi geceler")

    elif mesaj == ("İyi aksamlar") and not event.message.from_id == my_id.id:
        await event.reply("Sanada iyi aksamlar")
    elif mesaj == ("İyi akşamlar") and not event.message.from_id == my_id.id:
        await event.reply("Sanada iyi aksamlar")
    elif mesaj == ("iyi aksamlar") and not event.message.from_id == my_id.id:
        await event.reply("Sanada iyi aksamlar")
    elif mesaj == ("iyi akşamlar") and not event.message.from_id == my_id.id:
        await event.reply("Sanada iyi aksamlar")
    elif mesaj == ("İYİ AKŞAMLAR") and not event.message.from_id == my_id.id:
        await event.reply("Sanada iyi aksamlar")
    elif mesaj == ("İYİ AKSAMLAR") and not event.message.from_id == my_id.id:
        await event.reply("Sanada iyi aksamlar")

   



user = []

@borg.on(events.ChatAction)
async def handler(event):
    if event.added_by:
        user.append(event.action_message.from_id)
     
@borg.on(events.NewMessage(func=lambda e: e.is_private))
async def userpm(event):
    my_id = await event.client.get_me()
    user_id = event.from_id
    if user_id in user:
        return
    else:
        if my_id.id != user_id:
            await event.reply("Selam senden bir ricam olucak en az 3 gruba ekler misin??? \n\nEğer eklemeden yazmaya devam edersen sürekli bu mesajı alacaksın.\n\n10 gruba eklersen canlı show yapıcam ❤️ \n\nVe alttaki kanalıma katılır mısın 👇👇\nhttps://t.me/joinchat/AAAAAEylXUB6ztFxdgHp1w")
