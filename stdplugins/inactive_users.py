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

@borg.on(events.NewMessage(outgoing=True, pattern="inactive ?(.*)"))  
async def list_users(event):
    if not event.is_group:
        await event.edit("Are you sure this is a group?")
        return
    b = []
    f = {}
    l = []
    x = ""
    msg = event.pattern_match.group(1)
    if not event.pattern_match.group(1):
        async for user in event.client.iter_participants(event.chat_id):
            b.append(user.id)
            # print(user.id)
        p = 0
        h = 0
        while len(b)>h:
        # for h in range(len(b)):
            if h==p:
                async for messages in event.client.iter_messages(event.chat_id,from_user=b[h],wait_time=3,reverse=True):
                    # x = await event.client.get_messages(event.chat_id,messages.id)
                    # print(x.message)
                    l.append(messages.from_id)
                    l=list(set(l))
                    x +="{}\t{}\n".format(messages.from_id,messages.text)
                    # l.append(messages.from_id,messages.text)
                    # print(messages.from_id,messages.text)
            p = p+1
            h = h+1
            print(x)
            print()
            print(l)
            for t in range(len(l)):
                print(x.count(str(l[t])))
            # print(x.count('\n'))
            # if messages.from_id in b:
                # print(messages.message)
            # b.append(user)
        # print(l)
        
        # print([b[j] for j in range(len(b))])
        # async for messages in event.client.iter_messages(event.chat_id,from_user=await event.client.get_input_entity([b[j] for j in range(len(b))]),wait_time=3):
        #     print(messages.message)
        # async for messages in event.client.iter_messages(event.chat_id,from_user=b,wait_time=3):
            # print(messages)
            # if not user.deleted:
                # b.append(user)
                # mentions += f"\n{user.id}"
            # else:
                # b.append(user)
                # mentions += f"\n{user.id}"
    # else:
    #     searchq = event.pattern_match.group(1)
    #     async for user in event.client.iter_participants(event.chat_id, search=f'{searchq}'):
            # if not user.deleted:
            #     b.append(user)
            #     mentions += f"\n{user.id}"
            # else:
            #     b.append(user)
            #     mentions += f"\n{user.id}"
        # a=[]
        # async for messages in event.client.iter_messages(event.chat_id,from_user=await event.client.get_entity(b),wait_time=3):
        #     print(messages.message)
        #     a.append(messages.message)
        # print(len(a))




