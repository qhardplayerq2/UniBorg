# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from .uniborg import *
from sample_config import Config
from telethon.sessions import StringSession

if Config.HU_STRING_SESSION:
    session_name = str(Config.HU_STRING_SESSION)
    borg = Uniborg(
        StringSession(session_name),
        n_plugin_path="stdplugins/",
        db_plugin_path="dbplugins/",
        api_config=Config,
        api_id=Config.APP_ID,
        api_hash=Config.API_HASH
    )