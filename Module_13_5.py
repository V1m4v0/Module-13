from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import asyncio
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


api = ""
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

kb = ReplyKeyboardMarkup(resize_keyboard=True)
button = KeyboardButton( text = 'Рассчитать')
button2 = KeyboardButton( text = 'Информация')
kb.add(button)
kb.add(button2)

@dp.message_handler(commands='start')
async def start(message):
    await message.answer('Привет!', reply_markup = kb)


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()

@dp.message_handler(text = 'Рассчитать')
async def set_age(message):
    await message.answer('Введите свой возраст:')
    await UserState.age.set()

@dp.message_handler(state = UserState.age)
async def set_growth(message, state):
    await state.update_data(age = message.text)
    await message.answer('Введите свой рост:')
    await UserState.growth.set()

@dp.message_handler(state = UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth = message.text)
    await message.answer ('Введите свой вес:')
    await UserState.weight.set()

@dp.message_handler(state = UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight = message.text)
    data = await state.get_data()
    age = int(data['age'])
    growth = int(data['growth'])
    weight = int(data['weight'])
    calories = (weight * 10) + (6.25 * growth) - (5 * age) + 5
    await message.answer (f'Ваша норма калорий {calories} ккал в день')
    await state.finish()

@dp.message_handler()
async def all_message(message):
    await message.answer("Для начала работы введите команду /start")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
