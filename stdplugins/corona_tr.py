import asyncio

import requests

import wget
from sample_config import Config
from uniborg.util import admin_cmd
import os
from bs4 import BeautifulSoup

@borg.on(admin_cmd(pattern=("coronatr ?(.*)"))) # pylint:disable=E0602
async def cor_tr(event):
    x = await event.edit("`Corona virüs bilgileri sağlık bakanlığından alınıyor.`")
    await asyncio.sleep(3)
    if not os.path.isdir('./DOWNLOADS/'):
        os.makedirs('./DOWNLOADS/')
    r = requests.get(
    'https://covid19.saglik.gov.tr/')
    if r.status_code == 200:
        soup = BeautifulSoup(r.content, 'html.parser')
        res1 = soup.find_all("img",class_="img-fluid")
        resimler = []
        for image in res1:
            resimler.append(image['src'])
        re1 = resimler[2]
        resim1 = "https://covid19.saglik.gov.tr/{}".format(re1)
        res1 = requests.get(resim1)
        wget.download(res1, out='./DOWNLOADS/1.jpg')
        re2 = resimler[3]
        resim2 = "https://covid19.saglik.gov.tr/{}".format(re2)
        res2 = requests.get(resim2)
        wget.download(res2, out='./DOWNLOADS/2.jpg')
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
        img2 = Config.TMP_DOWNLOAD_DIRECTORY + '1.jpg'
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
        await x.edit("`Sağlık Bakanlığı sitesine erişilemiyor veya bir sorun var. Hata Kodu : 404`")

