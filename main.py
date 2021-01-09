import models
from config import *
import asyncio
from peewee import *
from aiogram.utils import executor
import datetime
import time, datetime
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.utils.executor import start_webhook
@dp.message_handler(commands=['start'])
async def start_msg(message: types.Message):
    if message.from_user.id == CHATID:
        await bot.send_message(message.from_user.id, 'Здарова пидрила', reply_markup = mainmenu)
@dp.message_handler()
async def main(message: types.Message):
    await bot.send_message(message.from_user.id, 'Здарова пидрила', reply_markup = mainmenu)
@dp.callback_query_handler(text = 'add_item')
async def adding(call: types.CallbackQuery):
    await bot.send_message(call.from_user.id, 'Введите Market Hash Name предмета')
    await add_item_state.name.set()
@dp.message_handler(state = add_item_state.name)
async def adding_name(message: types.Message, state: FSMContext):
    try:
        async with state.proxy() as data:
            current = market.get_lowest_price(message.text, AppID.CSGO)
            current = float(current[: current.find(" ") + 1].replace(',','.'))
            data['current'] = current
            data['name'] = message.text
            await bot.send_message(message.from_user.id, 'Введите сумму покупки')
            await add_item_state.next()
    except:
        await bot.send_message(message.from_user.id, 'Введите Market Hash Name ещё раз')
@dp.message_handler(state = add_item_state.buy_sum)
async def adding_buy_sum(message: types.Message, state: FSMContext):
    try:
        async with state.proxy() as data:
            data['buy_sum'] = float(message.text)
            await bot.send_message(message.from_user.id, 'Введите кол-во купленных ' + data['name'])
            await add_item_state.next()
    except:
        await bot.send_message(message.from_user.id, 'Введите сумму покупки ещё раз')
@dp.message_handler(state = add_item_state.count)
async def adding_count(message: types.Message, state: FSMContext):
    try:
        async with state.proxy() as data:
            data['count'] = int(message.text)
            item = models.Item(name = data['name'], buy_sum = data['buy_sum'], count = data['count'], current_sum = data['current'])
            item.save()
            await state.finish()
            await bot.send_message(message.from_user.id, 'Предмет успешно создан\nName: {}\nЦена покупки: {} руб.\nТекущая цена: {} руб.*\nКол-во: {}\nПрофит: {}%\n\n*С учётом комиссии ТП 13%'.format(data['name'], str(data['buy_sum']), str(round(data['current']*0.87, 2)), str(data['count']), str(round((round(data['current']*0.87, 2)/data['buy_sum'] - 1) * 100, 2))), reply_markup = add_again)
    except Exception as e:
        print(e)
        await bot.send_message(message.from_user.id, 'Введите кол-во купленных предметов ещё раз')
@dp.callback_query_handler(text = 'current_balance')
async def current(call: types.CallbackQuery):
    items = models.Item.select()
    txt = ''
    sum1 = 0
    for item in items:
        current = market.get_lowest_price(item.name, AppID.CSGO)
        current = float(current[: current.find(" ") + 1].replace(',','.'))
        item.current = current
        item.save()
        sum1+= round(current*0.87, 2)*item.count
        txt+= item.name + ' ('+str(round((round(current*0.87, 2)/item.buy_sum - 1) * 100, 2))+'%) ' + str(round(current*0.87, 2)) + ' pуб.\n\n'
    await bot.send_message(call.from_user.id, txt + 'Текущий баланс: ' + str(round(sum1, 2))+ ' руб.')

async def on_startup(dp):
    await bot.set_webhook(WEBHOOK_URL,drop_pending_updates=True)
async def on_shutdown(dp):
    pass
async def hook_set():
    if not HEROKU_APP_NAME:
        print('You have forgot to set HEROKU_APP_NAME')
        quit()
    await bot.set_webhook(WEBHOOK_URL)
    print(await bot.get_webhook_info())
start_webhook(
    dispatcher=dp,
    webhook_path=WEBHOOK_PATH,
    skip_updates=True,
    on_startup=on_startup,
    host=WEBAPP_HOST,
    port=WEBAPP_PORT,
)