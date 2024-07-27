from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.types import WebAppInfo
import os

API_TOKEN = os.getenv('API_TOKEN', '7439794203:AAEQGaP_uSsTh7c5onzP1VMrLo9VO1rmmtk')

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

allowed_users1 = ["vio_goncharova", "nft337"]
allowed_users2 = ["rjrizo", "nft337"]

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    user_id = message.from_user.id
    markup = types.ReplyKeyboardMarkup()
    markup.add(types.KeyboardButton('слово от RJ', web_app=WebAppInfo(
        url=f'https://rjrizokas.github.io/my-web-app-wordly/wordle.html?user_id={user_id}')))
    markup.add(types.KeyboardButton('слово от Ви', web_app=WebAppInfo(
        url=f'https://rjrizokas.github.io/my-web-app-wordly/wordle1.html?user_id={user_id}')))
    if message.from_user.username in allowed_users2:
        markup.add(types.KeyboardButton('загадать слово от RJ', web_app=WebAppInfo(
            url=f'https://rjrizokas.github.io/my-web-app-wordly/update.html?user_id={user_id}')))
    if message.from_user.username in allowed_users1:
        markup.add(types.KeyboardButton('загадать слово от Ви', web_app=WebAppInfo(
            url=f'https://rjrizokas.github.io/my-web-app-wordly/update1.html?user_id={user_id}')))
    await message.answer('Что наша жизнь?', reply_markup=markup)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
