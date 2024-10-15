from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import asyncio

api = ""
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

@dp.message_handler(commands = ['start'])
async def start(message):
    print(f'Привет! Я бот помогающий твоему здоровью.')
    await message.answer("Я нача    л работу, чем могу помочь?")

@dp.message_handler()
async def all_message(message):
    print(f'Введите команду /start, чтобы начать общение.')
    await message.answer("Для начала работы введите команду /start")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
