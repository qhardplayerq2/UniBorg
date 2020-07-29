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
            await event.reply("Selam, benimle konuşmak istiyorsan beni en az 1 gruba ekle eğer eklemeden yazmaya devam edersen sürekli bu mesajı alacaksın. \n\nVe alttaki kanalıma katılır mısın 👇👇\nhttps://t.me/joinchat/AAAAAEylXUB6ztFxdgHp1w")
