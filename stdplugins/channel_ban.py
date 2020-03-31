from asyncio import sleep
from os import remove
import asyncio
from telethon import events
from telethon.errors import (BadRequestError, ChatAdminRequiredError,
                             ImageProcessFailedError, PhotoCropSizeSmallError,
                             UserAdminInvalidError)
from telethon.errors.rpcerrorlist import (MessageTooLongError,
                                          UserIdInvalidError)
from telethon.tl.functions.channels import (EditAdminRequest,
                                            EditBannedRequest,
                                            EditPhotoRequest)
from telethon.tl.functions.messages import UpdatePinnedMessageRequest
from telethon.tl.types import (ChannelParticipantsAdmins,
                               ChannelParticipantsBots, ChatAdminRights,
                               ChatBannedRights, MessageEntityMentionName,
                               MessageMediaPhoto, PeerChat)

from sample_config import Config
from uniborg.util import admin_cmd

LOGGING_CHATID = Config.PRIVATE_GROUP_BOT_API_ID


ENABLE_LOG = True
LOGGING_CHATID = Config.PRIVATE_CHANNEL_BOT_API_ID
BANNED_RIGHTS = ChatBannedRights(
    until_date=None,
    view_messages=True,
    send_messages=True,
    send_media=True,
    send_stickers=True,
    send_gifs=True,
    send_games=True,
    send_inline=True,
    embed_links=True,
)


@borg.on(events.NewMessage(outgoing=True, pattern="^.cban(?: |$)(.*)")) # pylint:disable=E0602
async def ban(eventBan):
    if not eventBan.text[0].isalpha() and eventBan.text[0] not in ("/", "#", "@", "!"):
        # chat = await borg.get_input_entity(int("-1001425886003"))
        chat = await borg.get_entity(int("-1001106100161"))
        # print(chat)
        admin = chat.admin_rights
        creator = chat.creator
        if not admin and not creator:
            await eventBan.edit("`I am not an admin!`")
            return
        user = eventBan.pattern_match.group(1)
        if user:
            pass
        else:
            return
        await eventBan.edit("`Banlanacak kişiyi arıyorum...`")
        users = await borg.get_participants(chat)
        # print(users[0].id)
        try:
            await eventBan.client(
                EditBannedRequest(
                    chat.id,
                    users[0].id,
                    BANNED_RIGHTS
                )
            )
        except BadRequestError:
            await eventBan.edit("`I don't have sufficient permissions!`")
            return
        try:
            reply = await eventBan.get_reply_message()
            if reply:
                await reply.delete()
        except BadRequestError:
            await eventBan.edit("`I dont have message nuking rights! But still he was banned!`")
            return
        await eventBan.edit(f"[{user.first_name}](tg://user?id={user.id}) banlandı!")
        if ENABLE_LOG:
            await eventBan.client.send_message(
                LOGGING_CHATID,
                "#Channel_BAN\n"
                f"USER: [{users.first_name}](tg://user?id={users.id})\n"
                f"CHAT: `Kitap Arşivi Duyuru`"
            )


