
from db import *
from aiogram.types import ParseMode

from decouple import config


from datetime import datetime
import time

login_url = config("login_url")



def unix_time():
    dtime = datetime.now()
    unix_time = time.mktime(dtime.timetuple())
    return float(unix_time)




def unix_time():
    dtime = datetime.now()
    unix_time = time.mktime(dtime.timetuple())
    return float(unix_time)


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

def extract_unique_code(code: str):
    t = code.split()[1]
    return t


async def stater(message):
    # r = start.in_db(str(message.chat.id))
    r = bot_doc.find_one({"chat_id": str(message.chat.id)})
    if r:
        await message.reply("you have already registered")
    else:
        unique_code = extract_unique_code(message.text)
        print(f"this is unique code {unique_code}")
        if unique_code == None:
            rep = f"<a href='{login_url}/signup'>click me to signup </a>"
            await message.reply(rep, parse_mode=ParseMode.HTML)

        elif unique_code:  # if the '/start' command contains a unique_code

            # user = start.in_cache(unique_code)
            # user = bot_doc.find_one({"token" : str(unique_code)})
            user = in_cache(unique_code)
            print(user)

            if not isinstance(user, str) and user:  # if the username exists in our cache

                user.update({
                    "chat_id": str(message.chat.id),
                    "joined": unix_time(),
                    "balance": {
                        "berry": 0,
                        "zenni": 0
                    }
                })

                # start.save_chat_id(user)
                bot_doc.insert_one(user)
                await message.reply("Hello {0}, how are you?".format(user.get("dp_name")))

            elif user == None:
                rep = f"<a href='{login_url}/signup'>I have no clue who you are...\n Kindly follow me to signup </a>"
                await message.reply(rep, parse_mode=ParseMode.HTML)

            elif isinstance(user, str):
                rep = f"<a href='{login_url}/signup'>the token has expired kindly follow me to re-signup</a>"
                await message.reply(rep, parse_mode=ParseMode.HTML)

        else:
            await message.reply("Please visit me via the provided URL from the website.")
