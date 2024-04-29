from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ReplyKeyboardMarkup
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram import Bot, types
from config import bot_token
import sqlite3 as sq

from MessageText import HELP_COMMAND, HELLO_TEXT
from Weather import GetWeather

import logging

bot = Bot(token=bot_token)
dp = Dispatcher(bot, storage=MemoryStorage())
logger = logging.getLogger(__name__)
keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
buttons = ['Помощь', 'Новости', 'Курсы валют', 'Погода', 'Назад']
keyboard.add(*buttons)


class WeatherForm(StatesGroup):
    city = State()


class RateForm(StatesGroup):
    rate_symbol = State()


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await bot.send_message(
        reply_markup=keyboard,
        chat_id=message.from_user.id,
        text=HELLO_TEXT,
        parse_mode='HTML'
    )


@dp.message_handler(lambda message: message.text == 'Помощь')
async def process_help_command(message: types.Message):
    await bot.send_message(
        chat_id=message.from_user.id,
        text=HELP_COMMAND,
        parse_mode='HTML'
    )


@dp.message_handler(lambda message: message.text == 'Новости')
async def news_command(message: types.Message):
    conn = sq.connect("bot_helper.db")
    cur = conn.cursor()
    try:
        cur.execute('SELECT title, text, url FROM FinNews')
        for news in cur.fetchall():
            news_obj = f'\t{news[0]}\n{news[1]}\nИсточник: {news[2]}'
            await bot.send_message(message.from_id, news_obj)
    except:
        logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)
        logging.error(f'news_command {message.from_user.id}-{message.from_user.first_name}')
    finally:
        conn.close()


@dp.message_handler(lambda message: message.text == 'Курсы валют')
async def rate_handler(message: types.Message):
    await RateForm.rate_symbol.set()
    await message.answer('Введите символ валюты')


@dp.message_handler(lambda message: message.text == 'Погода')
async def weather_handler(message: types.Message):
    await WeatherForm.city.set()
    await message.answer("Введите название города")


@dp.message_handler(lambda message: message.text == 'Назад', state='*',)
@dp.message_handler(Text(equals='отмена', ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply('ОК')


@dp.message_handler(state='*', commands='cancel')
@dp.message_handler(Text(equals='отмена', ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply('ОК')


@dp.message_handler(state=WeatherForm.city)
async def weather_command(message: types.Message, state: FSMContext):
    try:
        for obj in GetWeather(message.text).__call__():
            await bot.send_message(message.from_id, obj)
    except:
        logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)
        logging.error(f'weather_command {message.from_user.id}-{message.from_user.first_name} -> {message.text}')
    finally:
        await state.finish()


@dp.message_handler(state=RateForm.rate_symbol)
async def rate_command(message: types.Message, state: FSMContext):
    symbol = message.text.replace(' ', '').upper()
    conn = sq.connect("bot_helper.db")
    cur = conn.cursor()
    try:
        cur.execute(f"SELECT rate_text, sum_rub FROM Rates WHERE rate_symbol = '{symbol}'")
        for rate in cur.fetchall():
            await bot.send_message(message.from_id, f'{rate[0]} в рублях = {rate[1]}')
            break
    except:
        logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)
        logging.error(f'rate_command {message.from_user.id}-{message.from_user.first_name} -> {symbol}')
        await message.answer('Простите но вы ввели несуществующий символ')
    finally:
        conn.close()
        await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
