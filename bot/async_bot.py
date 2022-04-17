from aiogram import Bot, types, executor, Dispatcher
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove, ParseMode

from datetime import datetime
from decouple import config

from db import *
from animesenai import entry
import general
from start import stater


login_url = config("login_url")
API_TOKEN = config("API_TOKEN")

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    # # r = start.in_db(str(message.chat.id))
    # r = bot_doc.find_one({"chat_id": str(message.chat.id)})
    # if r:
    #     await message.reply("you have already registered")
    # else:
    #     unique_code = start.extract_unique_code(message.text)
    #     print(f"this is unique code {unique_code}")
    #     if unique_code == None:
    #         rep = f"<a href='{login_url}/signup'>click me to signup </a>"
    #         await message.reply(rep, parse_mode=ParseMode.HTML)
    #
    #     elif unique_code:  # if the '/start' command contains a unique_code
    #
    #         # user = start.in_cache(unique_code)
    #         # user = bot_doc.find_one({"token" : str(unique_code)})
    #         user = in_cache(unique_code)
    #         print(user)
    #
    #         if not isinstance(user, str) and user:  # if the username exists in our cache
    #
    #             user.update({
    #                 "chat_id": str(message.chat.id),
    #                 "joined": general.unix_time(),
    #                 "balance": {
    #                     "berry": 0,
    #                     "zenni": 0
    #                 }
    #             })
    #
    #             # start.save_chat_id(user)
    #             bot_doc.insert_one(user)
    #             await message.reply("Hello {0}, how are you?".format(user.get("dp_name")))
    #
    #         elif user == None:
    #             rep = f"<a href='{login_url}/signup'>I have no clue who you are...\n Kindly follow me to signup </a>"
    #             await message.reply(rep, parse_mode=ParseMode.HTML)
    #
    #         elif isinstance(user, str):
    #             rep = f"<a href='{login_url}/signup'>the token has expired kindly follow me to re-signup</a>"
    #             await message.reply(rep, parse_mode=ParseMode.HTML)
    #
    #     else:
    #         await message.reply("Please visit me via the provided URL from the website.")
    await stater(message)


@dp.message_handler(commands=["news", "n"])
async def news(message: types.Message):
    if bot_doc.find_one({"chat_id": str(message.chat.id)}):

        e = {}
        for i in range(1, 5):
            try:
                e = entry()
            except:
                continue
            else:
                break

        for i in e:
            long_str = f"""
    <strong><a href="{i["link"]}">{i["title"]}</a></strong>
    {i["date"]}
    """

            await message.answer_photo(i["img"], caption=long_str, parse_mode=ParseMode.HTML)

    else:
        rep = f"<a href='{login_url}/signup'>click me to signup </a>"
        await message.reply(rep, parse_mode=ParseMode.HTML,reply_markup=remove_vote)


vote = types.ReplyKeyboardMarkup(resize_keyboard=True)
up = types.KeyboardButton('👍')
down = types.KeyboardButton('👎')
vote.add(up).add(down)


markup = types.ReplyKeyboardMarkup(row_width=2,resize_keyboard=True,one_time_keyboard=True)
itembtn1 = types.KeyboardButton('/pic')
itembtn2 = types.KeyboardButton('/name')
markup.add(itembtn1, itembtn2)

@dp.message_handler(commands=["help"])
async def help(msg: types.Message):

    if bot_doc.find_one({"chat_id": str(msg.chat.id)}):
        ret = open("help.txt","r")

        await bot.send_message(msg.chat.id, str(ret.read()), reply_markup=markup)
        ret.close()

        await bot.send_message(msg.chat.id, "Choose one letter:", reply_markup=markup)
    else:
        rep = f"<a href='{login_url}/signup'>click me to signup </a>"
        await msg.reply(rep, parse_mode=ParseMode.HTML,reply_markup=remove_vote)


# some code


remove_vote = ReplyKeyboardRemove()


# up = InlineKeyboardButton('👍', callback_data="1")
# down = InlineKeyboardButton('👎', callback_data="2")
# Up = InlineKeyboardMarkup(resize_keyboard=True, row_width=1).add(up).add(down)
# Down = InlineKeyboardMarkup(resize_keyboard=True, row_width=1).add(down)

vote = types.ReplyKeyboardMarkup(row_width=2,resize_keyboard=True,one_time_keyboard=True)
up = types.KeyboardButton('/news')
down = types.KeyboardButton('~saldodo')
vote.add(up, down)

@dp.message_handler(regexp="^~")
async def profile(message: types.Message):
    profile = message.text[1:]
    # rez = await search_col_doc(key="dp_name", query=profile)
    # rez = bot_db.search_one_col_sync("doc", key="dp_name", query=profile)
    rez = bot_doc.find_one({"dp_name": profile})
    if rez:
        import pprint
        pprint.pprint(rez)
        # if len(rez) == 1:
        if rez:
            image = bot_image.find_one({"file_name": rez["dp_pic"]})["image_url"]
            long_str = f"""
            name: {rez["dp_name"]}
            berry: {rez["balance"]["berry"]}
            zenni: {rez["balance"]["zenni"]}
            
            """

            await message.answer_photo(image, caption=long_str, reply_markup=markup)
        else:
            await message.answer(f"didn't see {profile} in db")

    else:
        await message.answer(f"didn't see {profile} in db")


def conf(massage: types.Message):
    if massage.text == '👎' or massage.text == '👍':
        return True
    return False


@dp.message_handler(conf)
async def vote(message: types.Message):
    await message.answer("yo")


@dp.message_handler(commands=['download', 'down'])
async def cmd_image(message: types.Message):
    await bot.send_photo(message.chat.id, types.InputFile.from_url(url))


@dp.message_handler()
async def echo(message: types.Message):
    await message.answer(message.text)


def greet():
    print("this is fun i just started runnin", str(datetime.utcnow()))


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=False, on_shutdown=greet())
