import re
from aiogram import types
from aiogram.types import WebAppInfo
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram.fsm.context import FSMContext

from core.callbacks.utils.subcategories import SubCategory

from core.data.SQLite_block import db


def get_keyboard_ADDLAMP_DELETE_EDIT_FORDEVS():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
        [types.KeyboardButton(text='Да'), types.KeyboardButton(text='Редактировать внесённые данные')],
        [types.KeyboardButton(text='Отменить действие')]
    ])
    return markup

def get_keyboard_UPDATE_FORDEVS():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
        [types.KeyboardButton(text='Да'), types.KeyboardButton(text='Изменить один параметр')],
        [types.KeyboardButton(text='Отменить действие')]
    ])
    return markup

def add_attr():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
        [types.KeyboardButton(text='Название')],
        [types.KeyboardButton(text='Мощность'), types.KeyboardButton(text='Стоимость')],
        [types.KeyboardButton(text='Ссылка'), types.KeyboardButton(text='Категория')]
    ])
    return markup

def get_quit():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
        [types.KeyboardButton(text='Отменить действие')]
    ])
    return markup

def get_keyboard_1lvl_branch():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
        [
            types.KeyboardButton(text='promishl'),
            types.KeyboardButton(text='SQuare'),
            types.KeyboardButton(text='street')
        ],
        [
            types.KeyboardButton(text='azs'),
            types.KeyboardButton(text='boom'),
            types.KeyboardButton(text='park')
        ],
        [
            types.KeyboardButton(text='ZHKH'),
            types.KeyboardButton(text='office'),
            types.KeyboardButton(text='arc')
        ]
    ])
    return markup

def get_keyboard_2lvl_branch(key):
    markup = ReplyKeyboardBuilder()
    for i in SubCategory[key]:
        markup.add(types.KeyboardButton(text=i))

    markup.adjust(4, 4, 4, 4)
    return markup.as_markup(resize_keyboard=True)

def get_keyboard_CONFIRM():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
        [types.KeyboardButton(text='Подтвердить')],
        [types.KeyboardButton(text='Отмена')]
    ])
    return markup

def get_keyboard_SEARCH(last):
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text=f'Показать ещё              Всего {last}', callback_data='more')
    return keyboard.as_markup()


async def get_keyboard_3lvl_branch(state: FSMContext, current=1):
    context_data = await state.get_data()
    subcategory = context_data.get('subcategory')
    sub_lamp = db.get_len_subcategory(subcategory)

    last = sub_lamp // 8
    if sub_lamp % 8 != 0:
        last += 1

    if current <= 0:
        current = last
    if current > last:
        current = 1

    page_num = (current - 1) * 8
    info = db.name_cost_by_category(subcategory, page_num)
    await state.update_data(current_page=current)

    def name_exists(information: list, index: int) -> tuple:
        try:
            res = information[index]
            for n in range(len(res[0])):
                if re.match(r'[a-zA-Z]', res[0][n]):
                    res = res[0][n:], str(res[1]) + '₽'
                    break
            else:
                res = '*', '*'
            return res
        except IndexError:
            return '*', '*'

    keyboard = InlineKeyboardBuilder()
    keyboard.button(text=f'{name_exists(info, 0)[0]} - {name_exists(info, 0)[1]}',
                    callback_data=f'{name_exists(info, 0)[0]}')
    keyboard.button(text=f'{name_exists(info, 1)[0]} - {name_exists(info, 1)[1]}',
                    callback_data=f'{name_exists(info, 1)[0]}')
    keyboard.button(text=f'{name_exists(info, 2)[0]} - {name_exists(info, 2)[1]}',
                    callback_data=f'{name_exists(info, 2)[0]}')
    keyboard.button(text=f'{name_exists(info, 3)[0]} - {name_exists(info, 3)[1]}',
                    callback_data=f'{name_exists(info, 3)[0]}')
    keyboard.button(text=f'{name_exists(info, 4)[0]} - {name_exists(info, 4)[1]}',
                    callback_data=f'{name_exists(info, 4)[0]}')
    keyboard.button(text=f'{name_exists(info, 5)[0]} - {name_exists(info, 5)[1]}',
                    callback_data=f'{name_exists(info, 5)[0]}')
    keyboard.button(text=f'{name_exists(info, 6)[0]} - {name_exists(info, 6)[1]}',
                    callback_data=f'{name_exists(info, 6)[0]}')
    keyboard.button(text=f'{name_exists(info, 7)[0]} - {name_exists(info, 7)[1]}',
                    callback_data=f'{name_exists(info, 7)[0]}')
    keyboard.button(text='<<', callback_data='previous')
    keyboard.button(text=f'{current}/{last}', callback_data='None')
    keyboard.button(text='>>', callback_data='next')
    keyboard.adjust(2, 2, 2, 2, 3)
    return keyboard.as_markup()

def get_keyboard_4lvl_branch(link):
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text='Перейти на сайт', web_app=WebAppInfo(url=link))
    return keyboard.as_markup()

def profile(id):
    keyboard = InlineKeyboardBuilder()
    keyboard.button(text='Профиль', url=f"tg://user?id={id}")
    return keyboard.as_markup()
