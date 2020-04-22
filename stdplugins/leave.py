import time

from telethon.tl.functions.channels import LeaveChannelRequest

from uniborg.util import admin_cmd


@borg.on(admin_cmd(pattern="leave", outgoing=True))
async def leave(e):
    await e.delete()
    time.sleep(3)
    if '-' in str(e.chat_id):
        await borg(LeaveChannelRequest(e.chat_id))
    else:
        pass
