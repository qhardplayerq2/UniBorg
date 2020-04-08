import logging
logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING)
from datetime import datetime
from uniborg.util import admin_cmd
from stdborg import borg

@borg.on(admin_cmd(pattern="ping")) 
async def _(event):
    if event.fwd_from:
        return
    start = datetime.now()
    await event.edit("Pong!")
    end = datetime.now()
    ms = (end - start).microseconds / 1000
    await event.edit("Pong!\n`{}`".format(ms))
