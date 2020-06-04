# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
"""Snips
Available Commands:
.snips
.snipl
.snipd"""
import logging

from telethon.tl import types

from database import settingsdb as settings
from database import snipsdb as nicedb
from sample_config import Config
from sql_helpers.snips_sql import (add_snip, get_all_snips, get_snips,
                                   remove_snip)
from uniborg.util import admin_cmd, arg_split_with, get_arg

logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING)
logger = logging.getLogger(__name__)


@borg.on(admin_cmd(pattern=r'\#(\S+)', outgoing=True))
async def watchout(message):
    if not await nicedb.check_one(message.text[1::]):
        return
    args = message.text
    if not await nicedb.check_others():
        if message.sender_id != (await message.client.get_me()).id:
            return
    if args.startswith("$"):
        argsraw = args[1::]
        snip = await nicedb.check_one(argsraw)
        value = (
            snip["Value"] if not snip["Media"]
            else await message.client.get_messages(await settings.check_asset(), ids=snip["Value"]))
        if not snip["Media"]:
            if message.sender_id == (await message.client.get_me()).id:
                await message.edit(value)
            else:
                await message.reply(value)
        else:
            if message.sender_id == (await message.client.get_me()).id:
                await message.client.send_message(message.chat_id, value)
                await message.delete()
            else:
                await message.client.send_message(message.chat_id, value, reply_to=message.id)


@borg.on(admin_cmd(pattern="snips (.*)"))
async def snipxxx(message):
    """Adds a snip into the list. Separate it with comma(,)"""
    args = arg_split_with(message, ",")
    reply = await message.get_reply_message()
    name = args[0]
    if len(args) == 0:
        await message.edit("**Enter the name of the snip first**")
        return
    if len(args) == 1 and not message.is_reply:
        await message.edit("**Enter or reply to a text to save as snip**")
        return
    if message.is_reply:
        if reply.media:
            value = (await message.client.send_message(await settings.check_asset(), reply)).id
            media = True
        else:
            value = reply.message
            media = False
    else:
        value = args[1]
        media = False
    if not await nicedb.check_one(name):
        await nicedb.add(name, value, media)
    else:
        await nicedb.update({"Key": name}, name, value, media)
    await message.edit(
        "**Snip **<i>{}</i>** successfully saved into the list."
        "Type **<i>${}</i>** to call it.**".format(name, name))


@borg.on(admin_cmd(pattern="snipl"))
async def snipsxxx(message):
    """Shows saved snips."""
    snips = ""
    get = await nicedb.check()
    if not get:
        await message.edit("**No snip found in snips list.**")
        return
    for snip in get:
        snips += "** ◍  " + snip["Key"] + "**\n"
    snipl = "**Snips that you saved: **\n\n" + snips
    await message.edit(snipl)


@borg.on(admin_cmd(pattern="snipd (\S+)"))
async def remsnipxxx(message):
    """Removes a snip from the list."""
    snipn = get_arg(message)
    if not snipn:
        await message.edit("**Please specify the name of the snip to remove.**")
        return
    if await nicedb.check_one(snipn):
        await nicedb.delete_one(snipn)
        await message.edit("**Snip **<i>{}</i>** successfully deleted**".format(snipn))
    else:
        await message.edit("**Snip **<i>{}</i>** not found in snips list**".format(snipn))


@borg.on(admin_cmd(pattern="snipdl"))
async def remsnipsxxx(message):
    """Clears out the snip list."""
    if not await nicedb.check():
        await message.edit("**There are no snips in the list to clear out.**")
        return
    await nicedb.delete()
    await message.edit("**All snips successfully removed from the list.**")
