"""Quickly make a decision
Syntax: .decide"""
import logging

import requests

from uniborg.util import admin_cmd

logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING)

@borg.on(admin_cmd(pattern="decide")) # pylint:disable=E0602
async def _(event):
    if event.fwd_from:
        return
    message_id = event.message.id
    if event.reply_to_msg_id:
        message_id = event.reply_to_msg_id
    r = requests.get("https://yesno.wtf/api").json()
    await borg.send_message(
        event.chat_id,
        r["answer"],
        reply_to=message_id,
        file=r["image"]
    )
    await event.delete()
