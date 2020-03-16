"""
Turkish word meaning. Only Turkish. Coded @By_Azade
"""

import logging
import os
from datetime import datetime
from telethon import events
from sample_config import Config
from uniborg.util import admin_cmd
import requests
import json

logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING)

@borg.on(admin_cmd(pattern="tdk ?(.*)"))
async def tdk(event):
    if event.fwd_from:
        return
    inp = event.pattern_match.group(1)
    # inp = input("kelime:")
    kelime = "https://sozluk.gov.tr/gts?ara={}".format(inp)
    headers = {"USER-AGENT": "UniBorg"}
    response = requests.get(kelime, headers=headers).json()
    anlam_sayisi = response[0]['anlam_say']
    # anlam_1 = response[0]['anlamlarListe'][0]['anlam']
    # anlam_2 = response[0]['anlamlarListe'][1]['anlam']
    try:
        x = "TDK Sözlük\n"
        for anlamlar in range(int(anlam_sayisi)):
            x += "-{}\n".format(response[0]['anlamlarListe'][anlamlar]['anlam'])
            # print(x)
        await event.edit(x)
    except KeyError:
        await event.edit(KeyError)