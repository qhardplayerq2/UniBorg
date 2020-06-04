from database.mongo import cli

cli = cli["Userbot"]["Lydia"]


async def add_lydia(colname, user_id, chat_id, session_id, session_expires):
    return cli[colname].insert_one(
        {"User_ID": user_id, "Chat_ID": chat_id, "Session_ID": session_id, "Session_Expires": session_expires})


async def check_lydia(colname, chat):
    return [x for x in cli[colname].find({"Chat": chat})]

async def delete_lydia(colname, user_id, chat_id):
    return cli[colname].delete_many({"User_ID": user_id, "Chat_ID": chat_id})

