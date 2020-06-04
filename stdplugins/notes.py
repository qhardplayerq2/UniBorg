import logging

from database import notesdb as nicedb
from database import settingsdb as settings
from sample_config import Config
from uniborg.util import admin_cmd, arg_split_with, get_arg, reply

logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING)
logger = logging.getLogger(__name__)

MONGO_DB_URI = Config.MONGO_DB_URI


@borg.on(admin_cmd(pattern='savenote (.*)', outgoing=True))
async def savexxx(message):
    if not MONGO_DB_URI:
        await message.edit("`Database connections failing!`")
        return
    args = arg_split_with(message, ",")
    storage = await settings.check_asset()
    media = None
    reply = await message.get_reply_message()
    if not args:
        await message.edit("**You need to enter a note name**")
        return
    if len(args) == 1 and not message.is_reply:
        await message.edit(
            "**You need to either enter a a text or reply to a message to save as note**")
        return
    value = reply.text if message.is_reply else " ".join(args[1:])
    name = args[0]
    chatid = message.chat_id
    if reply and reply.media and not reply.web_preview:
        media = (await message.client.send_message(storage, reply)).id
    if await nicedb.check_one("Notes", chatid, name):
        await nicedb.update("Notes", {"Chat": chatid, "Key": name},
                            chatid, name, value, media)
        await message.edit("**Note succesfully updated**")
    else:
        await nicedb.add("Notes", chatid, name, value, media)
        await message.edit("**Note succesfully saved**")


@borg.on(admin_cmd(pattern='notes (.*)', outgoing=True))
async def notesxxx(message):
    if not MONGO_DB_URI:
        await message.edit("`Database connections failing!`")
        return
    chatid = message.chat_id
    notes = await nicedb.check("Notes", chatid)
    if not notes:
        await message.edit("**No notes found in this chat**")
        return
    caption = "**Notes you saved in this chat:\n\n**"
    list = ""
    for note in notes:
        list += "**  ◍ " + note["Key"] + "**\n"
    caption += list
    await message.edit(caption)


@borg.on(admin_cmd(pattern='delnotes (.*)', outgoing=True))
async def clearxxx(message):
    if not MONGO_DB_URI:
        await message.edit("`Database connections failing!`")
        return
    args = get_arg(message)
    chatid = message.chat_id
    if not await nicedb.check_one("Notes", chatid, args):
        await message.edit("**No notes found in that name**")
        return
    await nicedb.delete_one("Notes", chatid, args)
    await message.edit("**Note deleted successfully**")


@borg.on(admin_cmd(pattern='deleteallnotes (.*)', outgoing=True))
async def clearallxxx(message):
    if not MONGO_DB_URI:
        await message.edit("`Database connections failing!`")
        return
    chatid = message.chat_id
    if not await nicedb.check("Notes", chatid):
        await message.edit("**There are no notes in this chat**")
        return
    await nicedb.delete("Notes", chatid)
    await message.edit("**Notes cleared out successfully**")


# @borg.on(admin_cmd(pattern='notechk (.*)', outgoing=True))
@borg.on(admin_cmd(incoming=True))
async def watchout(message):
    if not MONGO_DB_URI:
        await message.edit("`Database connections failing!`")
        return
    arg = message.text[1::]
    chatid = message.chat_id
    storage = await settings.check_asset()
    note = await nicedb.check_one("Notes", chatid, arg)
    if not note:
        return
    fetch = None if not note["Media"] else await message.client.get_messages(entity=storage, ids=note["Media"])
    if hasattr(fetch, "media"):
        await reply(message, fetch)
        return
    await message.reply(note["Value"])
