from aiogram import *
from aiogram.dispatcher import Dispatcher
from aiogram.types import *
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from telethon.sync import TelegramClient
from telethon import functions
from steam_community_market import Market, AppID
import asyncio
import os


BOT_TOKEN = os.getenv('BOT_TOKEN')
if not BOT_TOKEN:
    print('You have forgot to set BOT_TOKEN')
    quit()

HEROKU_APP_NAME = os.getenv('HEROKU_APP_NAME')


# webhook settings
WEBHOOK_HOST = f'https://{HEROKU_APP_NAME}.herokuapp.com'
WEBHOOK_PATH = f'/webhook/{BOT_TOKEN}'
WEBHOOK_URL = f'{WEBHOOK_HOST}{WEBHOOK_PATH}'

# webserver settings
WEBAPP_HOST = '0.0.0.0'
WEBAPP_PORT = int(os.getenv('PORT')
CHATID = 357536913
FE = 0.13
storage = MemoryStorage()
bot = Bot(token='1511765201:AAGHNpZK7S4Pz8jiG29IlQ6cv9vC5uttl6o')
dp = Dispatcher(bot, storage=storage)
back = InlineKeyboardButton('Назад', callback_data= 'back')
mainmenu = InlineKeyboardMarkup()
mainmenu.add(InlineKeyboardButton('Добавить предмет', callback_data = 'add_item'))
mainmenu.add(InlineKeyboardButton('Удалить Предмет',callback_data = 'del_item'))
mainmenu.add(InlineKeyboardButton('Текущий баланс', callback_data = 'current_balance'))
market = Market('RUB')
add_again = InlineKeyboardMarkup()
add_again.add(InlineKeyboardButton('Добавить ещё предмет', callback_data = 'add_item'))
add_again.add(back)
class add_item_state(StatesGroup):
    name = State()
    buy_sum = State()
    count = State()
