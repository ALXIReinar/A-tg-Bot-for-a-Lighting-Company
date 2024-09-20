from aiogram import types, Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.types import WebAppInfo

from core.config import TOKEN, HELP, HELP_FOR_DEVS, SEARCH_HELP, START
from core.commands import set_commands, set_dev_commands
from core.data.SQLite_block import db


bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode='HTML'))
dp = Dispatcher()


async def start(message: types.Message):

    await message.answer(f'<code>Hi</code>, {message.from_user.first_name}!\n' + START,
                         reply_markup=types.ReplyKeyboardRemove(remove_keyboard=True))

    res = db.user_exists(message.from_user.id)
    if len(res):

        status = res[0][2]
        if status:
            await set_dev_commands(bot)
        else:
            await set_commands(bot)

    else:

        tg_id = message.from_user.id
        db.add_user(tg_id)
        await set_commands(bot)

    await menu(message)


async def menu(message: types.Message):
    markup = types.InlineKeyboardMarkup(inline_keyboard=[
        [
         types.InlineKeyboardButton(text='Промышленные', callback_data='Promishl'),
         types.InlineKeyboardButton(text='Для Торговых площадей', callback_data='SellSquare'),
         types.InlineKeyboardButton(text="Уличные", callback_data='Street')
         ],
        [
         types.InlineKeyboardButton(text='Для АЗС', callback_data='AZS'),
         types.InlineKeyboardButton(text='Взрывозащищённые', callback_data='Explosion'),
         types.InlineKeyboardButton(text='Парковые', callback_data='Park')
        ],
        [
         types.InlineKeyboardButton(text='Для ЖКХ', callback_data='ZHKH'),
         types.InlineKeyboardButton(text='Офисные', callback_data='Office'),
         types.InlineKeyboardButton(text='Архитектурные', callback_data='Architecture')
        ],
        [types.InlineKeyboardButton(text='Перейти на сайт', url='https://deledzavod.ru/katalog/')]
    ])

    await message.answer('Выберите категорию светильников:', reply_markup=markup)


async def website(message: types.Message):
    pic = 'https://deledzavod.ru/katalog/'
    markup = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text='Перейти на сайт', web_app=WebAppInfo(url='https://deledzavod.ru/katalog/'))]])
    await message.answer(f'Сайт: {pic}', reply_markup=markup)


async def user_help(message: types.Message):
    await message.answer(HELP, reply_markup=types.ReplyKeyboardRemove(remove_keyboard=True))

async def dev_help(message: types.Message):
    await message.answer(HELP_FOR_DEVS, reply_markup=types.ReplyKeyboardRemove(remove_keyboard=True))


async def search_help(message: types.Message):
    await message.answer(SEARCH_HELP, reply_markup=types.ReplyKeyboardRemove(remove_keyboard=True))


async def users(message: types.Message):
    text = ''
    info = db.all_users()
    print(info)
    for i in range(len(info)):
        id = f'Id: <code>{info[i][0]}</code>  Статус - '
        status = f'{info[i][1]}'
        if bool(status):
            status = f'<b><i>{status}</i></b>'
        text += id + status

    await message.answer(text)