from database.mongo import cli

cli = cli["Userbot"]["Lydia"]


async def add_lydia(user_id, chat_id, session_id, session_expires):
    return cli.insert_one(
        {"User_ID": user_id, "Chat_ID": chat_id, "Session_ID": session_id, "Session_Expires": session_expires})


async def get_lydia(user_id, chat_id):
    return cli.find_one(
        {"User_ID": user_id, "Chat_ID": chat_id})


async def check_lydia(chat):
    return [x for x in cli.find({"Chat": chat})]


async def delete_lydia(user_id, chat_id):
    return cli.delete_many({"User_ID": user_id, "Chat_ID": chat_id})


# async def check_user(user_id, chat_id):
#     return (True if not cli.find_one({"User_ID": user_id}) and not cli.find_one({"Chat_ID": chat_id})
