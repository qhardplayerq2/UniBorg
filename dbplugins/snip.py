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

# from sql_helpers.snips_sql import (add_snip, get_all_snips, get_snips,
#                                    remove_snip)
import io
from stdplugins.dphelper import add_note, get_note, get_notes, delete_note
from uniborg.util import admin_cmd
from sample_config import Config, is_mongo_alive, is_redis_alive

logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING)
logger = logging.getLogger(__name__)


@borg.on(admin_cmd(pattern=r'\#(\S+)', outgoing=True))
async def on_snip(event):
    name = event.pattern_match.group(1)
    if not is_mongo_alive() or not is_redis_alive():
        await event.edit("`Database connections failing!`")
        return
    snip = get_note(event.chat_id, name)
    if snip:
        msg_o = await event.client.get_messages(
            entity=Config.PRIVATE_CHANNEL_BOT_API_ID,
            ids=int(snip["text"])
        )
        message_id = event.message.id
        if event.reply_to_msg_id:
            message_id = event.reply_to_msg_id
        media_message = msg_o.media
        if isinstance(media_message, types.MessageMediaWebPage):
            media_message = None
        await event.reply(
            msg_o,
            reply_to=message_id
        )
        await event.delete()


@borg.on(admin_cmd(pattern="snips (.*)"))
async def on_snip_save(event):
    if not is_mongo_alive() or not is_redis_alive():
        await event.edit("`Database connections failing!`")
        return
    name = event.pattern_match.group(1)
    msg = await event.get_reply_message()
    if msg:
        msg_o = await event.client.forward_messages(
            entity=Config.PRIVATE_CHANNEL_BOT_API_ID,
            messages=msg,
            from_peer=event.chat_id,
            silent=True
        )
        # add_note(name, msg_o.id)
        note = add_note(event.chat_id, name, msg)
        await event.edit("snip {name} saved successfully. Get it with #{name}".format(name=note["text"]))
    else:
        await event.edit("Reply to a message with `snips keyword` to save the snip")


@borg.on(admin_cmd(pattern="snipl"))
async def on_snip_list(event):
    if not is_mongo_alive() or not is_redis_alive():
        await event.edit("`Database connections failing!`")
        return
    all_snips = get_notes(event.chat_id)
    OUT_STR = "Available Snips:\n"
    if len(all_snips["name"]) > 0:
        for a_snip in all_snips["name"]:
            OUT_STR += f"👉 #{a_snip.snip} \n"
    else:
        OUT_STR = "No Snips. Start Saving using `.snips`"
    if len(OUT_STR) > Config.MAX_MESSAGE_SIZE_LIMIT:
        with io.BytesIO(str.encode(OUT_STR)) as out_file:
            out_file.name = "snips.text"
            await event.client.send_file(
                event.chat_id,
                out_file,
                force_document=True,
                allow_cache=False,
                caption="Available Snips",
                reply_to=event
            )
            await event.delete()
    else:
        await event.edit(OUT_STR)


@borg.on(admin_cmd(pattern="snipd (\S+)"))
async def on_snip_delete(event):
    if not is_mongo_alive() or not is_redis_alive():
        await event.edit("`Database connections failing!`")
        return
    name = event.pattern_match.group(1)
    # remove_snip(name)
    delete_note(event.chat_id, name)
    if await delete_note(event.chat_id, name) is False:
        return await event.edit("`Couldn't find note:` **{}**".format(name)
                                )
    else:
        return await event.edit(
            "`Successfully deleted note:` **{}**".format(name))
    await event.edit("snip #{} deleted successfully".format(name))
