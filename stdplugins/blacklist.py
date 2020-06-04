import logging

from database import blacklistdb as blacklist
from uniborg.util import admin_cmd

logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)


@borg.on(admin_cmd(pattern='blacklistchat (.*)', outgoing=True))
async def blacklistxxx(message):
    chat = message.chat_id
    await blacklist.add_blacklist(chat)
    await message.edit("<i>This chat is now blacklisted</i>")


@borg.on(admin_cmd(pattern='whitelistchat (.*)', outgoing=True))
async def whitelistxxx(message):
    chat = message.chat_id
    if await blacklist.check_blacklist(chat):
        await blacklist.delete_blacklist(chat)
        await message.edit("<i>This chat is now whitelisted</i>")
    else:
        await message.edit("<i>This chat is already whitelisted</i>")
