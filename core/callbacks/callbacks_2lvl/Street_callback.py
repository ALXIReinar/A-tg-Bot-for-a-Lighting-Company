from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.utils.media_group import MediaGroupBuilder


async def answer_Street(call: types.CallbackQuery):
    def get_keyboard():
        keyboard = InlineKeyboardBuilder()
        keyboard.button(text='Optimus-S', callback_data='street_optimus-s')
        keyboard.button(text='Optimus-S-Lite', callback_data='street_optimus-s-lite')
        keyboard.button(text='Long-S', callback_data='street_long-s')
        keyboard.button(text='Optimus Cast', callback_data='street_optimus-cast')
        keyboard.adjust(2, 2)
        return keyboard.as_markup()

    photo_Street = MediaGroupBuilder()
    photo_Street.add(
        type='photo',
        media='https://sun9-68.userapi.com/impg/mwVuIyFy4gaE9Rxkr1fU2BOrvaNPi-3uvW_f0A/iZ10OEmrOJ0.jpg?size=1920x899&quality=96&sign=65f51e872467a01e75f6372d2c2a3042&type=album',
        caption='Optimus-S'
    )
    photo_Street.add(
        type='photo',
        media='https://sun9-39.userapi.com/impg/-qyJ0ooulAcKQ0Ogjzbu_da7u8mMhvvUceMf_g/uWqCqBY3H9Y.jpg?size=2560x1517&quality=96&sign=ff8af967a5bfea07a0bb44ad5c209d47&type=album',
        caption='Optimus-S-Lite'
    )
    photo_Street.add(
        type='photo',
        media='https://sun9-71.userapi.com/impg/lgkIi2BwcZ9X35HIFSk0BFxsdbDsk_h4H9SAEg/gBrfB9N-k8U.jpg?size=1147x554&quality=96&sign=183cefbebd66e7b5e75193c3df4555b8&type=album',
        caption='Long-S'
    )
    photo_Street.add(
        type='photo',
        media='https://sun9-75.userapi.com/impg/eiO-D82FodlzUalqCtNfteoWSPzQB_cD8ui1mQ/iUdpylJy2uQ.jpg?size=886x886&quality=96&sign=6b8b3e1236d64186d3f47697736771a1&type=album',
        caption='Optimus Cast'
    )
    await call.message.answer_media_group(media=photo_Street.build())
    await call.message.answer('Выберите тип светильника:', reply_markup=get_keyboard())
