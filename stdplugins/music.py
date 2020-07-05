"get music from .m <music query>  Credits https://t.me/By_Azade"
import logging

from telethon import events
from telethon.errors.rpcerrorlist import (UserAlreadyParticipantError,
                                          YouBlockedUserError)
from telethon.tl.functions.account import UpdateNotifySettingsRequest

from uniborg.util import admin_cmd, humanbytes

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
    msg = await event.get_reply_message()
    await event.delete()

    music_name = event.pattern_match.group(1)
    msg = await event.get_reply_message()
    if music_name:
        await event.delete()
        song_result = await event.client.inline_query("spotify_to_mp3_bot", music_name)

        for res in range(len(song_result)):

            if "(FLAC)" in song_result[res].title:

                j = await song_result[res].click(event.chat_id, reply_to=event.reply_to_msg_id, hide_via=True)
                k = await event.respond(j)
                await j.delete()
                await k.edit("Kanal Linki:\nhttps://t.me/joinchat/AAAAAE8NqbV48l7ls-pFtQ")
                break

            elif "(MP3_320)" in song_result[res].title:

                j = await song_result[res].click(event.chat_id, reply_to=event.reply_to_msg_id, hide_via=True)
                k = await event.respond(j)
                await j.delete()
                await k.edit("Kanal Linki:\nhttps://t.me/joinchat/AAAAAE8NqbV48l7ls-pFtQ")
                break

            elif "(MP3_128)" in song_result[res].title:

                j = await song_result[res].click(event.chat_id, reply_to=event.reply_to_msg_id, hide_via=True)
                k = await event.respond(j)
                await j.delete()
                await k.edit("Kanal Linki:\nhttps://t.me/joinchat/AAAAAE8NqbV48l7ls-pFtQ")
                break

    elif msg:

        await event.delete()
        song_result = await event.client.inline_query("spotify_to_mp3_bot", msg.message)
        for res in range(len(song_result)):

            if "(FLAC)" in song_result[res].title:

                j = await song_result[res].click(event.chat_id, reply_to=event.reply_to_msg_id, hide_via=True)
                k = await event.respond(j)
                await j.delete()
                await k.edit("Kanal Linki:\nhttps://t.me/joinchat/AAAAAE8NqbV48l7ls-pFtQ")
                break

            elif "(MP3_320)" in song_result[res].title:

                j = await song_result[res].click(event.chat_id, reply_to=event.reply_to_msg_id, hide_via=True)
                k = await event.respond(j)
                await j.delete()
                await k.edit("Kanal Linki:\nhttps://t.me/joinchat/AAAAAE8NqbV48l7ls-pFtQ")
                break

            elif "(MP3_128)" in song_result[res].title:

                j = await song_result[res].click(event.chat_id, reply_to=event.reply_to_msg_id, hide_via=True)
                k = await event.respond(j)
                await j.delete()
                await k.edit("Kanal Linki:\nhttps://t.me/joinchat/AAAAAE8NqbV48l7ls-pFtQ")
                break


@events.register(events.NewMessage(pattern="ad ?(.*)", outgoing=True))
async def _(event):
    if event.fwd_from:
        return
    if not event.reply_to_msg_id:
        await event.edit("```Reply to any user message.```")
        return
    reply_message = await event.get_reply_message()
    if not reply_message.media:
        await event.edit("```reply to media message```")
        return
    chat = "@audiotubebot"
    sender = reply_message.sender
    if reply_message.sender.bot:
        await event.edit("```Reply to actual users message.```")
        return
    await event.edit("```Processing```")
    async with event.client.conversation(chat) as conv:
        try:
            response = conv.wait_event(events.NewMessage(
                incoming=True, from_users=507379365))
            await event.client.send_message(chat, reply_message)
            response = await response
        except YouBlockedUserError:
            await event.reply("```Please unblock @AudioTubeBot and try again```")
            return
        await event.delete()
        await event.client.send_file(event.chat_id, response.message.media)


@borg.on(admin_cmd(pattern="fm ?(.*)"))  # pylint:disable=E0602
async def _(event):
    msg = await event.get_reply_message()
    await event.delete()
    if msg:
        msj = f"[{msg.file.name[0:-5]}](https://t.me/joinchat/AAAAAE8NqbV48l7ls-pFtQ)\n`{humanbytes(msg.file.size)}`"
        await event.client.send_message(
            entity=await event.client.get_entity(-1001326295477),
            file=msg.media,
            message=msj
        )
    else:
        await event.edit("`mesajı yanıtla`")
