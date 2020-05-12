import asyncio
import logging

from telethon import events, functions, types

from sample_config import Config
from uniborg.util import admin_cmd

logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING)
logger = logging.getLogger(__name__)


@borg.on(admin_cmd(pattern=("sil ?(.*)")))  # pylint:disable=E0602
async def _(event):
    chat = await event.get_chat()
    await event.client.delete_dialog(chat.id)
