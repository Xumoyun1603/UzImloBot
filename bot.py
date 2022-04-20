import logging
from aiogram import Bot, Dispatcher, executor, types
from checkWord import checkWord
from transliterate import to_cyrillic, to_latin

from environs import Env

env = Env()
env.read_env()

API_TOKEN = env.str('API_TOKEN')

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("UzImlo Botiga Xush Kelibsiz!")


@dp.message_handler(commands=['help'])
async def help_user(message: types.Message):
    await message.reply("Botdan foydalanish uchun so'z yuboring.")


@dp.message_handler()
async def checkImlo(message: types.Message):
    msg = message.text
    if msg.isascii():
        msg = to_cyrillic(msg)

    words = set(msg.split(' '))
    if '' in words:
        words.remove('')

    for word in words:
        result = checkWord(word)
        if result['available']:
            response = f"✅ {word.capitalize()}"
        else:
            response = f"❌ {word.capitalize()}\n"
            for text in result['matches']:
                response += f"✅ {text.capitalize()}"

        await message.answer(response)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)