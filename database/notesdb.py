import logging
from database.mongo import cli


cli = cli["Userbot"]


async def add(colname, chat, key, value, media):
    return cli[colname].insert_one(
        {"Chat": chat, "Key": key, "Value": value, "Media": media})


async def check(colname, chat):
    return [x for x in cli[colname].find({"Chat": chat})]


async def check_one(colname, chat, key):
    return cli[colname].find_one({"Chat": chat, "Key": key})


async def update(colname, query, chat, key, value, media):
    return cli[colname].update_one(
        query, {"$set": {"Chat": chat, "Key": key, "Value": value, "Media": media}})


async def delete(colname, chat):
    return cli[colname].delete_many({"Chat": chat})


async def delete_one(colname, chat, key):
    return cli[colname].delete_one({"Chat": chat, "Key": key})
