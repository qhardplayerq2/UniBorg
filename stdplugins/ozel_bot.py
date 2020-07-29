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
    if mesaj == "selam" or "Selam" and not event.message.from_id == my_id.id:
        await event.reply("selammm")
    elif mesaj == "Sea" or "sea" or "sa" or "Sa" or "SA" and not event.message.from_id == my_id.id:
        await event.reply("ase")    
    elif mesaj == "naber" or "Naber" or "nbr" or "Nbr" or "NBR" and not event.message.from_id == my_id.id:
        await event.reply("iyidir senden naber")
    elif mesaj == "napıyon" or "Napıyon" or "ne yapıyorsun" or "napıyorsun" and not event.message.from_id == my_id.id:
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
