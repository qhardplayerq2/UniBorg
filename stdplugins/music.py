"get music from .m <music query>  Credits https://t.me/By_Azade"

import asyncio
import logging

from telethon.errors.rpcerrorlist import (UserAlreadyParticipantError,
                                          YouBlockedUserError)
from telethon.tl.functions.account import UpdateNotifySettingsRequest
from telethon.tl.functions.messages import ImportChatInviteRequest

from sample_config import Config
from uniborg.util import admin_cmd

logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING)
logger = logging.getLogger(__name__)


@borg.on(admin_cmd(pattern="music ?(.*)"))  # pylint:disable=E0602
async def music_find(event):
    if event.fwd_from:
        return

    music_name = event.pattern_match.group(1)
    msg = await event.get_reply_message()
    if music_name:
        await event.delete()
        song_result = await event.client.inline_query("deezermusicbot", music_name)

        await song_result[0].click(
            event.chat_id,
            reply_to=event.reply_to_msg_id,
            hide_via=True
        )
    elif msg:
        await event.delete()
        song_result = await event.client.inline_query("deezermusicbot", msg.message)

        await song_result[0].click(
            event.chat_id,
            reply_to=event.reply_to_msg_id,
            hide_via=True
        )


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

        await song_result[1].click(event.chat_id, reply_to=event.reply_to_msg_id, hide_via=True)

    elif msg:
        await event.delete()
        song_result = await event.client.inline_query("spotify_to_mp3_bot", msg.message)

        await song_result[1].click(event.chat_id, reply_to=event.reply_to_msg_id, hide_via=True)


@borg.on(admin_cmd(pattern="xx ?(.*)"))
async def _(event):
    if event.fwd_from:
        return
    await event.edit("`müzik indiriliyor, birazdan gönderilecek.`")
    d_link = event.pattern_match.group(1)
    bot = "@spotify_to_mp3_bot"

    async with event.client.conversation("@spotify_to_mp3_bot") as conv:
        try:
            await conv.send_message(d_link)
            await asyncio.sleep(2)

            details = await conv.get_response()
            await asyncio.sleep(2.75)
            x = await details.click(0)
            await asyncio.sleep(1)
            details_2 = await conv.get_response()
            y = await details_2.click(1)
            await asyncio.sleep(1)
            details_3 = await conv.get_response()
            await asyncio.sleep(3.75)
            await event.client.send_file(event.chat_id, details_3.media, caption="Kanal Linki:\nhttps://t.me/joinchat/AAAAAE8NqbV48l7ls-pFtQ")
        except YouBlockedUserError:
            await event.edit("**Error:** `unblock` @spotify_to_mp3_bot `and retry!`")
        except TypeError:
            await asyncio.sleep(2)
            await event.client.send_file(event.chat_id, details_3.media, caption="Kanal Linki:\nhttps://t.me/joinchat/AAAAAE8NqbV48l7ls-pFtQ")
    await event.delete()
