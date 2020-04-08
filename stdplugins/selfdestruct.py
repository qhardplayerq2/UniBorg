"""Self Destruct Plugin
.sd <time in seconds> <text>
"""
import time

from uniborg.util import admin_cmd

@borg.on(admin_cmd(pattern="sd", outgoing=True  )) # pylint:disable=E0602
async def selfdestruct(destroy):
    """ For .sd command, make seflf-destructable messages. """
    if not destroy.text[0].isalpha() and destroy.text[0] not in ("/", "#", "@", "!"):
        message = destroy.text
        counter = int(message[4:6])
        text = str(destroy.text[6:])
        text = (
            text
            + "\n\n`Bu mesaj "
            + str(counter)
            + " saniye sonunda silinecektir.`"
        )
        await destroy.delete()
        smsg = await destroy.client.send_message(destroy.chat_id, text)
        time.sleep(counter)
        await smsg.delete()
