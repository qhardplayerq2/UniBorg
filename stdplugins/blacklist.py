import logging

from database import blacklistdb as blacklist
from uniborg.util import admin_cmd

logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)


@borg.on(admin_cmd(pattern='blacklistchat (.*)', outgoing=True))
async def blacklistxxx(message):
    chat = message.chat_id
    await blacklist.add_blacklist(chat)
    await message.edit("__This chat is now blacklisted__")


@borg.on(admin_cmd(pattern='whitelistchat (.*)', outgoing=True))
async def whitelistxxx(message):
    chat = message.chat_id
    if await blacklist.check_blacklist(chat):
        await blacklist.delete_blacklist(chat)
        await message.edit("__This chat is now whitelisted__")
    else:
        await message.edit("__This chat is already whitelisted__")
