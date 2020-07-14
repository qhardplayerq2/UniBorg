import logging
from datetime import datetime

from uniborg.util import admin_cmd, edit_or_reply

logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING)
logger = logging.getLogger(__name__)


@borg.on(admin_cmd(pattern="ping"))
async def _(event):
    if event.fwd_from:
        return
    ed = await edit_or_reply(event, "...")
    start = datetime.now()
    j = await ed.edit("Pong!")
    end = datetime.now()
    ms = (end - start).microseconds / 1000
    await j.edit("Pong!\n`{}`".format(ms))
