from aiogram import Bot, Dispatcher, types
from aiogram.utils.executor import start_webhook
from aiohttp import web

import logging
import os

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

API_TOKEN = os.getenv('API_TOKEN', '7439794203:AAEQGaP_uSsTh7c5onzP1VMrLo9VO1rmmtk')  # Установите ваш API токен

WEBHOOK_HOST = os.getenv('RENDER_EXTERNAL_URL', 'https://my-web-app-wordly-tg.onrender.com')  # URL вашего сервиса на Render
WEBHOOK_PATH = '/webhook'
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

allowed_users1 = ["vio_goncharova", "nft337"]
allowed_users2 = ["rjrizo", "nft337"]

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    user_id = message.from_user.id
    markup = types.ReplyKeyboardMarkup()
    markup.add(types.KeyboardButton('слово от RJ', web_app=types.WebAppInfo(
        url=f'https://rjrizokas.github.io/my-web-app-wordly/wordle.html?user_id={user_id}')))
    markup.add(types.KeyboardButton('слово от Ви', web_app=types.WebAppInfo(
        url=f'https://rjrizokas.github.io/my-web-app-wordly/wordle1.html?user_id={user_id}')))
    if message.from_user.username in allowed_users2:
        markup.add(types.KeyboardButton('загадать слово от RJ', web_app=types.WebAppInfo(
            url=f'https://rjrizokas.github.io/my-web-app-wordly/update.html?user_id={user_id}')))
    if message.from_user.username in allowed_users1:
        markup.add(types.KeyboardButton('загадать слово от Ви', web_app=types.WebAppInfo(
            url=f'https://rjrizokas.github.io/my-web-app-wordly/update1.html?user_id={user_id}')))
    await message.answer('Что наша жизнь?', reply_markup=markup)

async def on_startup(dp):
    try:
        await bot.set_webhook(WEBHOOK_URL)
        logger.info(f"Webhook set to {WEBHOOK_URL}")
    except Exception as e:
        logger.error(f"Failed to set webhook: {e}")

async def on_shutdown(dp):
    try:
        await bot.delete_webhook()
        logger.info("Webhook deleted")
    except Exception as e:
        logger.error(f"Failed to delete webhook: {e}")

async def handle_root(request):
    return web.Response(text="Hello, this is the root endpoint!")

app = web.Application()
app.router.add_get('/', handle_root)

# Настройка вебхука и других обработчиков

if __name__ == '__main__':
    port = int(os.getenv('PORT', 10000))  # Render автоматически установит значение PORT
    logger.info(f"Starting webhook on port {port}")
    start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        skip_updates=True,
        host='0.0.0.0',
        port=port
    )
