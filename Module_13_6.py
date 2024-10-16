from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import asyncio
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


api = ""
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

kb = ReplyKeyboardMarkup(resize_keyboard=True)
button = KeyboardButton(text='Рассчитать')
button2 = KeyboardButton(text='Информация')
kb.add(button)
kb.add(button2)

il_kb = InlineKeyboardMarkup()
il_button = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')
il_button2 = InlineKeyboardButton(text='Формулы расчёта', callback_data='formulas')
il_kb.add(il_button)
il_kb.add(il_button2)

class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()

@dp.message_handler(commands=['start'])
async def start(message):
    await message.answer('Привет, я бот рассчитывающий калории!', reply_markup=kb)

@dp.message_handler(text = 'Рассчитать')
async def main_menu(message):
    await message.answer('Выберите опцию', reply_markup=il_kb)

@dp.callback_query_handler(text = ['formulas'])
async def get_formulas(call):
    await call.message.answer(f'Формула для расчета калорий: 10*вес(кг) + 6,25*рост(см) - 5*возраст(г)- 161')
    await call.answer()

@dp.callback_query_handler(text = ['calories'])
async def set_age(call):
    await call.message.answer('Введите свой возраст:')
    await call.answer()
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
    calories = (weight * 10) + (6.25 * growth) - (5 * age) - 161
    await message.answer (f'Ваша норма калорий {calories} ккал в день')
    await state.finish()

@dp.message_handler()
async def all_message(message):
    await message.answer("Для начала работы введите команду /start")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
