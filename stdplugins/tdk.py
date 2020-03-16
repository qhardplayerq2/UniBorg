# """
# Turkish word meaning. Only Turkish. Coded @By_Azade
# """

# import logging
# import os
# from datetime import datetime
# from telethon import events
# from sample_config import Config
# from uniborg.util import admin_cmd
# # from tdk.core import TurkishWord
# from tdk import tdk
# logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
#                     level=logging.WARNING)

# @borg.on(admin_cmd(pattern="tdk ?(.*)"))
# async def tdk(event):
#     if event.fwd_from:
#         return
#     kelime = event.pattern_match.group(1)
#     word = tdk.new_word(kelime)
#     sonuc = word.all_data()
#     await event.edit(sonuc)