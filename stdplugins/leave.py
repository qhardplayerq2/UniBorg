
from uniborg.util import admin_cmd


@borg.on(admin_cmd(pattern="leave", outgoing=True))
async def leave(e):
    await e.delete()
    await e.client.kick_participant(e.chat_id, 'me')
