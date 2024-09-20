from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.utils.media_group import MediaGroupBuilder


async def answer_Architecture(call: types.CallbackQuery):
    def get_keyboard():
        keyboard = InlineKeyboardBuilder()
        keyboard.button(text='Long-Arc', callback_data='arc_long')
        keyboard.button(text='Alfa', callback_data='arc_alfa')
        keyboard.button(text='Dion', callback_data='arc_dion')
        keyboard.button(text='Optimus-Arc', callback_data='arc_optimus')
        keyboard.button(text='Mirage-Arc', callback_data='arc_mirage')
        keyboard.adjust(2, 2, 1)
        return keyboard.as_markup()

    photos_Architecture = MediaGroupBuilder()
    photos_Architecture.add(
        type='photo',
        caption='Long-Arc',
        media='https://deledzavod.ru/katalog/arhitekturnoe-osveshhenie/long-arc-20-l06-optic/'
    )
    photos_Architecture.add(
        type='photo',
        caption='Alfa',
        media='https://deledzavod.ru/katalog/arhitekturnoe-osveshhenie/alfa-spot-d1-5/'
    )
    photos_Architecture.add(
        type='photo',
        caption='Dion',
        media='https://deledzavod.ru/katalog/arhitekturnoe-osveshhenie/dion-arh-l05/'
    )
    photos_Architecture.add(
        type='photo',
        caption='Optimus-Arc',
        media='https://deledzavod.ru/katalog/arhitekturnoe-osveshhenie/optimus-arc-30-optic/'
    )
    photos_Architecture.add(
        type='photo',
        caption='Mirage-Arc',
        media='https://deledzavod.ru/katalog/arhitekturnoe-osveshhenie/mirage-arc-35-optic/'
    )

    await call.message.answer_media_group(media=photos_Architecture.build())
    await call.message.answer('Выберите тип светильника:', reply_markup=get_keyboard())
    await call.answer()
