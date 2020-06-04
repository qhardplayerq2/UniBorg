import logging

from database.notesdb import add_note, delete_note, get_note, get_notes
from database import settingsdb as settings
from sample_config import Config
from uniborg.util import admin_cmd, arg_split_with, get_arg, reply

logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING)
logger = logging.getLogger(__name__)

MONGO_DB_URI = Config.MONGO_DB_URI


@borg.on(admin_cmd(pattern='savenote (.*)', outgoing=True))
async def add_filter(event):
    """ For .save command, saves notes in a chat. """
    if not MONGO_DB_URI:
        await event.edit("`Database connections failing!`")
        return

    notename = event.pattern_match.group(1)
    string = event.text.partition(notename)[2]
    if event.reply_to_msg_id:
        string = " " + (await event.get_reply_message()).text

    msg = "`Note {} successfully. Use` #{} `to get it`"

    if await add_note(event.chat_id, notename, string[1:]) is False:
        return await event.edit(msg.format('updated', notename))
    else:
        return await event.edit(msg.format('added', notename))


@borg.on(admin_cmd(pattern='notes (.*)', outgoing=True))
async def notes_active(event):
    """ For .notes command, list all of the notes saved in a chat. """
    if not MONGO_DB_URI:
        await event.edit("`Database connections failing!`")
        return

    message = "`There are no saved notes in this chat`"
    notes = await get_notes(event.chat_id)
    for note in notes:
        if message == "`There are no saved notes in this chat`":
            message = "Notes saved in this chat:\n"
            message += "🔹 **{}**\n".format(note["name"])
        else:
            message += "🔹 **{}**\n".format(note["name"])

    await event.edit(message)


@borg.on(admin_cmd(pattern='delnote (.*)', outgoing=True))
async def remove_notes(event):
    """ For .clear command, clear note with the given name."""
    if not MONGO_DB_URI:
        await event.edit("`Database connections failing!`")
        return
    notename = event.pattern_match.group(1)
    if await delete_note(event.chat_id, notename) is False:
        return await event.edit("`Couldn't find note:` **{}**".format(notename)
                                )
    else:
        return await event.edit(
            "`Successfully deleted note:` **{}**".format(notename))


# @borg.on(admin_cmd(pattern='notechk (.*)', outgoing=True))
@borg.on(admin_cmd(incoming=True))
async def note(event):
    """ Notes logic. """
    try:
        if not (await event.get_sender()).bot:
            if not MONGO_DB_URI:
                return

            notename = event.text[1:]
            note = await get_note(event.chat_id, notename)
            if note:
                await event.reply(note["text"])
    except BaseException:
        pass
