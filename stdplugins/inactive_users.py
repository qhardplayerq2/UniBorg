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


KICK_RIGHTS = ChatBannedRights(
    until_date=None,
    view_messages=True
)

@borg.on(events.NewMessage(outgoing=True, pattern="^.inactive ?(.*)"))  
async def list_users(event):
    if not event.is_group:
        await event.edit("Are you sure this is a group?")
        return
    info = await event.client.get_entity(event.chat_id)
    title = info.title if info.title else "this chat"
    mentions = '\n'
    b = []
    msg = event.pattern_match.group(1)
    try:
        if not event.pattern_match.group(1):
            async for user in event.client.iter_participants(event.chat_id):
                if not user.deleted:
                    b.append(user)
                    mentions += f"\n{user.id}"
                else:
                    b.append(user)
                    mentions += f"\n{user.id}"
        else:
            searchq = event.pattern_match.group(1)
            async for user in event.client.iter_participants(event.chat_id, search=f'{searchq}'):
                if not user.deleted:
                    b.append(user)
                    mentions += f"\n{user.id}"
                else:
                    b.append(user)
                    mentions += f"\n{user.id}"
            a=[]
            async for messages in event.client.iter_messages(event.chat_id,from_user=await event.client.get_entity(b)):
                print(messages.message)
                a.append(messages.message)
            print(len(a))
            if len(a)<msg:
                chat = await event.get_chat()
                admin = chat.admin_rights
                creator = chat.creator
                if not admin and not creator:
                    await event.edit("`I am not an admin!`")
                    return
                user = await get_user_from_event(event)
                if not user:
                    await event.edit("`Couldn't fetch user.`")
                    return
                await event.edit("`Kicking this users...`")
                try:
                    await event.client(
                        EditBannedRequest(
                            event.chat_id,
                            user.id,
                            KICK_RIGHTS
                        )
                    )
                    await sleep(.5)
                except BadRequestError:
                    await event.edit("`I don't have sufficient permissions!`")
                    return
                await event.client(
                    EditBannedRequest(
                        event.chat_id,
                        user.id,
                        ChatBannedRights(until_date=None)
                    )
                )
                await event.edit(f"[{user.first_name}](tg://user?id={user.id})` `atıldı` !`")
    except ChatAdminRequiredError as err:
        mentions += " " + str(err) + "\n"
    try:
        await event.edit(mentions)
    except MessageTooLongError:
        await event.edit("Damn, this is a huge group. Uploading users lists as file.")
        file = open("userslist.txt", "w+")
        file.write(mentions)
        file.close()
        await event.client.send_file(
            event.chat_id,
            "userslist.txt",
            caption='Users in {}'.format(title),
            reply_to=event.id,
        )
        remove("userslist.txt")



async def get_user_from_event(event):
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        user_obj = await event.client.get_entity(previous_message.from_id)
    else:
        user = event.pattern_match.group(1)
        if user.isnumeric():
            user = int(user)
        if not user:
            await event.edit("`Pass the user's username, id or reply!`")
            return
        if event.message.entities is not None:
            probable_user_mention_entity = event.message.entities[0]

            if isinstance(probable_user_mention_entity, MessageEntityMentionName):
                user_id = probable_user_mention_entity.user_id
                user_obj = await event.client.get_entity(user_id)
                return user_obj
        try:
            user_obj = await event.client.get_entity(user)
        except (TypeError, ValueError) as err:
            await event.edit(str(err))
            return None
    return user_obj

async def get_user_from_id(user, event):
    if isinstance(user, str):
        user = int(user)
    try:
        user_obj = await event.client.get_entity(user)
    except (TypeError, ValueError) as err:
        await event.edit(str(err))
        return None
    return user_obj



