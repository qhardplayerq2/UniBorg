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
    if mesaj == "selam" and not event.message.from_id == my_id.id:
        await event.reply("selam canım")
    elif mesaj == "naber" and not event.message.from_id == my_id.id:
        await event.reply("iyidir senden naber")


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
            await event.reply("Selam, benimle konuşmak istiyorsan beni en az 1 gruba eklemeden yazmaya devam edersen sürekli bu mesajı alacaksın.")
