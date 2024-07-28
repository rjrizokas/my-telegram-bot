from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.types import WebAppInfo
import os
from aiohttp import web
import asyncio


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
        markup.add(types.KeyboardButton('редактор словаря', web_app=WebAppInfo(
        url=f'https://rjrizokas.github.io/my-web-app-wordly/add_word.html')))
    await message.answer('Что наша жизнь?', reply_markup=markup)

async def handle_root(request):
    return web.Response(text="Hello! The bot is running.", content_type='text/html')

if __name__ == '__main__':
    app = web.Application()
    app.router.add_get('/', handle_root)
    
    runner = web.AppRunner(app)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(runner.setup())
    
    site = web.TCPSite(runner, '0.0.0.0', int(os.getenv('PORT', 10000)))
    loop.run_until_complete(site.start())
    
    executor.start_polling(dp, skip_updates=True)
