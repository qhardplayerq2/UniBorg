import logging

from database import notesdb as nicedb
from database import settingsdb as settings
from uniborg.util import admin_cmd, arg_split_with, get_arg

BLACKLIST = [".stop", ".stopall", ".filter"]


logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)


@borg.on(admin_cmd(pattern='filter (.*)', outgoing=True))
async def filterxxx(message):
    args = arg_split_with(message, ",")
    storage = await settings.check_asset()
    media = None
    reply = await message.get_reply_message()
    if not args:
        await message.edit("<b>You need to enter a filter name</b>")
        return
    if len(args) == 1 and not message.is_reply:
        await message.edit("<b>You need to either enter a a text or reply to a message to save as filter</b>")
        return
    if message.is_reply:
        value = reply.text
    else:
        value = " ".join(args[1:])
    name = args[0]
    chatid = message.chat_id
    if reply and reply.media and not reply.web_preview:
        media = (await message.client.send_message(storage, reply)).id
    if await nicedb.check_one("Filters", chatid, name):
        await nicedb.update("Filters", {"Chat": chatid, "Key": name},
                            chatid, name, value, media)
        await message.edit("<b>Filter succesfully updated</b>")
    else:
        await nicedb.add("Filters", chatid, name, value, media)
        await message.edit("<b>Filter succesfully saved</b>")


@borg.on(admin_cmd(pattern='listfilters (.*)', outgoing=True))
async def filtersxxx(message):
    chatid = message.chat_id
    filters = await nicedb.check("Filters", chatid)
    if not filters:
        await message.edit("<b>No filter found in this chat</b>")
        return
    caption = "<b>Word(s) you filtered in this chat:\n\n</b>"
    list = ""
    for filter in filters:
        list += "<b>  ◍ " + filter["Key"] + "</b>\n"
    caption += list
    await message.edit(caption)


@borg.on(admin_cmd(pattern='stopfilter (.*)', outgoing=True))
async def stopxxx(message):
    args = get_arg(message)
    chatid = message.chat_id
    if not await nicedb.check_one("Filters", chatid, args):
        await message.edit("<b>No filter found in that name</b>")
        return
    await nicedb.delete_one("Filters", chatid, args)
    await message.edit("<b>Filter deleted successfully</b>")


@borg.on(admin_cmd(pattern='stopallfilter (.*)', outgoing=True))
async def stopallxxx(message):
    chatid = message.chat_id
    if not await nicedb.check("Filters", chatid):
        await message.edit("<b>There are no filters in this chat</b>")
        return
    await nicedb.delete("Filters", chatid)
    await message.edit("<b>Filters cleared out successfully</b>")


@borg.on(admin_cmd(incoming=True))
async def watchout(message):
    for i in BLACKLIST:
        if message.text.startswith(i):
            return
    arg = message.text
    chatid = message.chat_id
    storage = await settings.check_asset()
    filters = await nicedb.check("Filters", chatid)
    if not filters:
        return
    for item in filters:
        if item["Key"] in arg:
            value = item["Value"] if not item["Media"] else item["Media"]
            if item["Media"]:
                fetch = await message.client.get_messages(entity=storage, ids=value)
                await message.client.send_message(chatid, fetch, reply_to=message.id)
                return
            await message.reply(value)
