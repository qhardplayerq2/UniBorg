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
    await event.edit("müzik indiriliyor, birazdan gönderilecek.")
    d_link = event.pattern_match.group(1)
    # if ".com" not in d_link:
    #     await event.edit("` I need a link to download something pro.`**(._.)**")
    # else:
    #     await event.edit("🎶**Initiating Download!**🎶")
    bot = "@spotify_to_mp3_bot"

    async with event.client.conversation("@spotify_to_mp3_bot") as conv:
        try:
            # await conv.send_message("/start")
            # response = await conv.get_response()
            # print(response)
            # try:
            #     await event.client(ImportChatInviteRequest('AAAAAFZPuYvdW1A8mrT8Pg'))
            # except UserAlreadyParticipantError:
            #     await asyncio.sleep(0.00000069420)
            await conv.send_message(d_link)
            await asyncio.sleep(2)
            details = await conv.get_response()
            # print(details.reply_markup)
            # for a in range(len(details.reply_markup.rows)):
            #     # details_1 = await conv.get_response()
            #     if  details.buttons[a][0].text in d_link:
            #         # x = await details_1.click(0)
            #         print(details)
            #     # print(details.buttons[a][0].text)
            await asyncio.sleep(3)
            # print(details)
            x = await details.click(0)
            # print(x)
            # print("-------------------------------------------------------------------------")
            await asyncio.sleep(1)
            details_2 = await conv.get_response()
            y = await details_2.click(1)
            # print(y)
            # print("-------------------------------------------------------------------------")
            print(details_2)
            # print("-------------------------------------------------------------------------")
            await asyncio.sleep(1)
            details_3 = await conv.get_response()
            # print(details_3)
            # print("-------------------------------------------------------------------------")
            await asyncio.sleep(2.5)
            # await event.client.send_message(event.chat_id, details)
            # await conv.get_response()
            # songh = await conv.get_response()
            await event.client.send_file(event.chat_id, details_3.media, caption="Kanal Linki:\nhttps://t.me/joinchat/AAAAAE8NqbV48l7ls-pFtQ")
            # await event.delete()
        except YouBlockedUserError:
            await event.edit("**Error:** `unblock` @spotify_to_mp3_bot `and retry!`")
