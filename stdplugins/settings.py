import logging

from database import settingsdb as settings
from sample_config import Config
from uniborg.util import admin_cmd, get_arg

logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)


@borg.on(admin_cmd(pattern='setprefix (.*)', outgoing=True))
async def setprefixxxx(message):
    if not Config.MONGO_DB_URI:
        await message.edit("`Database connections failing!`")
        return
    pref = get_arg(message)
    await settings.delete("Prefix")
    await settings.set_prefix(pref)
    await message.edit("<b>Prefix has been successfully set to: {}</b>".format(pref))
