from pymongo import MongoClient
from general import *
from decouple import config


string = config("db_string")

def conn_sync():
    while True:
        try:
            client_sync = MongoClient(string)
        except:
            continue
        else:
            return client_sync.bot


sync_bot = MongoClient(string)
db = sync_bot["bot"]
bot_cache = db["cache"]
bot_doc = db["doc"]
bot_image = db["image"]





def in_cache(unique_code):
    # check_unique = bot_db.search_one_col_sync("cache",key="token",query=unique_code)
    check_unique = bot_cache.find_one({"token": unique_code})
    if check_unique:

        time_check = unix_time() - float(check_unique["time"])
        if time_check > 600.0:
            bot_cache.delete_one({"token": unique_code})

            return "the token is old"
        elif time_check < 600.0:
            bot_cache.delete_one({"token": unique_code})
            data = {
                    "token": check_unique["token"],
                    "username": check_unique["username"],
                    "password": check_unique["password"],
                    "dp_name": check_unique["dp_name"],
                    "dp_pic": check_unique["dp_pic"]
                    }
            return data

    return None



