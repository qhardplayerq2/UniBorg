import logging
import re
from asyncio import sleep

from database import settingsdb as settings
from database.filtersdb import add_filter, delete_filter, get_filters
from sample_config import Config
from uniborg.util import admin_cmd, arg_split_with, get_arg

BLACKLIST = [".stop", ".stopall", ".filter"]


logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)


@borg.on(admin_cmd(pattern='filter (.*)', outgoing=True))
async def add_new_filter(event):
    """ Command for adding a new filter """
    if not Config.MONGO_DB_URI:
        await event.edit("`Database connections failing!`")
        return
    message = event.text
    keyword = message.split()
    string = ""
    for i in range(2, len(keyword)):
        string = string + " " + str(keyword[i])

    if event.reply_to_msg_id:
        string = " " + (await event.get_reply_message()).text

    msg = "`Filter `**{}**` {} successfully`"

    if await add_filter(event.chat_id, keyword[1], string[1:]) is True:
        await event.edit(msg.format(keyword[1], 'added'))
    else:
        await event.edit(msg.format(keyword[1], 'updated'))


@borg.on(admin_cmd(pattern='listfilters', outgoing=True))
async def filters_active(event):
    """ For .filters command, lists all of the active filters in a chat. """
    if not Config.MONGO_DB_URI:
        await event.edit("`Database connections failing!`")
        return
    transact = "`There are no filters in this chat.`"
    filters = await get_filters(event.chat_id)
    for filt in filters:
        if transact == "`There are no filters in this chat.`":
            transact = "Active filters in this chat:\n"
            transact += " • **{}** - `{}`\n".format(filt["keyword"],
                                                    filt["msg"])
        else:
            transact += " • **{}** - `{}`\n".format(filt["keyword"],
                                                    filt["msg"])

    await event.edit(transact)


@borg.on(admin_cmd(pattern='stopfilter (.*)', outgoing=True))
async def remove_filter(event):
    """ Command for removing a filter """
    if not Config.MONGO_DB_URI:
        await event.edit("`Database connections failing!`")
        return
    filt = event.text[6:]

    if not await delete_filter(event.chat_id, filt):
        await event.edit("`Filter `**{}**` doesn't exist.`".format(filt))
    else:
        await event.edit(
            "`Filter `**{}**` was deleted successfully`".format(filt))


@borg.on(admin_cmd(incoming=True))
async def filter_incoming_handler(handler):
    """ Checks if the incoming message contains handler of a filter """
    try:
        if not (await handler.get_sender()).bot:
            if not Config.MONGO_DB_URI:
                await handler.edit("`Database connections failing!`")
                return

            filters = await get_filters(handler.chat_id)
            if not filters:
                return
            for trigger in filters:
                pattern = r"( |^|[^\w])" + re.escape(
                    trigger["keyword"]) + r"( |$|[^\w])"
                if re.search(pattern, handler.text, flags=re.IGNORECASE):
                    await handler.reply(trigger["msg"])
                    return
    except AttributeError:
        pass
