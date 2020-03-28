import asyncio

import requests

import wget
from sample_config import Config
from uniborg.util import admin_cmd
import os


@borg.on(admin_cmd(pattern=("coronatr ?(.*)"))) # pylint:disable=E0602
async def cor_tr(event):
    await event.edit("`Corona virüs bilgileri sağlık bakanlığından alınıyor.`")
    await asyncio.sleep(3)
    if not os.path.isdir('./DOWNLOADS/'):
        os.makedirs('./DOWNLOADS/')
    r = requests.get(
    'https://covid19.saglik.gov.tr/')
    if r.status_code == 200:
        resim1 = "https://covid19.saglik.gov.tr/1.png"
        res1 = requests.get(resim1)
        if res1.status_code == 200:
            wget.download(resim1, out='./DOWNLOADS/1.png')
        resim2 = "https://covid19.saglik.gov.tr/2.jpg"
        res2 = requests.get(resim2)
        if res2.status_code == 200:
            wget.download(resim2, out='./DOWNLOADS/2.jpg')
        img1 = Config.TMP_DOWNLOAD_DIRECTORY + '2.jpg'
        await event.client.send_file(
            event.chat_id,
            img1,
            force_document=False,
            allow_cache=False,
            caption="Sağlık Bakanlığı Corona Virüs Güncel Bilgiler Grafiği",
            reply_to=event
        )
        await  asyncio.sleep(4)
        img2 = Config.TMP_DOWNLOAD_DIRECTORY + '1.png'
        await event.client.send_file(
            event.chat_id,
            img2,
            force_document=False,
            allow_cache=False,
            caption="Sağlık Bakanlığı Corona Virüs Güncel Bilgiler Tablosu",
            reply_to=event
        )
        os.remove(img1)
        await asyncio.sleep(3)
        os.remove(img2)
    else:
        await event.edit("`Sağlık Bakanlığı sitesine erişilemiyor veya bir sorun var. Hata Kodu : 404`")

