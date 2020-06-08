"get music from .m <music query>  Credits https://t.me/By_Azade"

import logging

from sample_config import Config
from uniborg.util import admin_cmd

logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING)
logger = logging.getLogger(__name__)


@borg.on(admin_cmd(pattern="m ?(.*)"))  # pylint:disable=E0602
async def music_find(event):
    if event.fwd_from:
        return

    music_name = event.pattern_match.group(1)
    msg = await event.get_reply_message()
    if music_name:
        await event.delete()
        song_result = await event.client.inline_query("deezermusicbot", music_name)

        await event.respond(await song_result[0].click(
            event.chat_id,
            reply_to=event.reply_to_msg_id,
            hide_via=True
        ))
    elif msg:
        await event.delete()
        song_result = await event.client.inline_query("deezermusicbot", msg.message)

        await event.respond(await song_result[0].click(
            event.chat_id,
            reply_to=event.reply_to_msg_id,
            hide_via=True
        ))


@borg.on(admin_cmd(pattern="spotbot ?(.*)"))  # pylint:disable=E0602
async def _(event):
    if event.fwd_from:
        return
    # msg = await event.get_reply_message()
    # print(msg)
    music_name = event.pattern_match.group(1)
    msg = await event.get_reply_message()
    # print(event)
    if music_name:
        await event.delete()
        song_result = await event.client.inline_query("spotify_to_mp3_bot", music_name)
        await event.respond(
            await song_result[1].click(event.chat_id, reply_to=event.reply_to_msg_id, hide_via=True)
        )
    elif msg:
        await event.delete()
        song_result = await event.client.inline_query("spotify_to_mp3_bot", msg.message)

        await event.respond(
            await song_result[1].click(event.chat_id, reply_to=event.reply_to_msg_id, hide_via=True)
        )