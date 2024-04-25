import cohere
from aiogram import Bot, types
from aiogram import Dispatcher
from aiogram.filters import CommandStart, Command
import json
import asyncio

bot = Bot(token='6361712914:AAFXzAnByEwX-xssUmI-WzX7Ksf_gS_ThwE', parse_mode="Markdown")
dp = Dispatcher()

history = {}

def get_answer(text: str):
    co = cohere.Client(
      api_key="OF9dYtzlD6c1yefSMHbVdMDoZFUNW5Cy7oKjvFxB",
    )

    chat = co.chat(
        message=text,
        model="command"
    )

    return chat.text


@dp.message(CommandStart())
async def command_start_handler(message) -> None:
    await message.answer(f"Hello, {message.from_user.full_name}!")


@dp.message(Command('help'))
async def help_handler(message) -> None:
    await message.answer("Help:\n\t 1. /help - show user-help manual\n\t 2. /start - launch bot\n\t 3. /save - save whole dialog")


@dp.message(Command('save'))
async def save_handler(message) -> None:
    await message.answer("Dialog saved!")
    with open('dialog.json', 'w') as js:
        json.dump(history, js, indent=4)


@dp.message()
async def echo_handler(message: types.Message):
    cohere_message = 'Answer'
    if message.chat.id not in history.keys():
        history[message.chat.id] = []
    else:
        history[message.chat.id].append({
            'User': message.text,
            'Bot': cohere_message
        })
    await message.answer(cohere_message)

asyncio.run(dp.start_polling(bot))
