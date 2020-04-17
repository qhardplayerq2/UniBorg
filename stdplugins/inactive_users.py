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

    try:
        msg = event.pattern_match.group(1)
        mesaj = "Grupta {} mesajı olmayanlar otomatik olarak çıkarılıyor..\nBu uzun sürebilir".format(msg)
        await event.edit(mesaj)
        b = []
        f = {}
        l = []
        x = ""
        msg = event.pattern_match.group(1)
        # if not event.pattern_match.group(1):
        async for user in event.client.iter_participants(event.chat_id):
            # print(user)
            if not user.bot:
                # print(user.first_name)
                b.append(user.id)
            # print(user.id)
        p = 0
        h = 0
        while len(b)>h:
        # for h in range(len(b)):
            if h==p:
                async for messages in event.client.iter_messages(event.chat_id,from_user=b[h],reverse=True):
                    l.append(messages.from_id)
                    l=list(set(l))
                    x +="{}\t{}\n".format(messages.from_id,messages.text)
            p = p+1
            h = h+1
            liste = []
            for t in range(len(l)):
                liste.append(x.count(str(l[t])))
            for j in range(len(l)):
                if int(liste[j]) < int(msg):
                    l.append(l[j])
                    l=list(set(l))
                    print(l[j])
                    await event.client(
                        EditBannedRequest(
                            event.chat_id,
                            l[j],
                            KICK_RIGHTS
                        )
                    )
    except BadRequestError as bad:
        await event.edit(str(bad))
    except ChatAdminRequiredError as ch:
        await event.edit(str(ch))
        


async def ban_user(chat_id, i, rights):
    try:
        await borg(functions.channels.EditBannedRequest(chat_id, i, rights))
        return True, None
    except Exception as exc:
        return False, str(exc)

