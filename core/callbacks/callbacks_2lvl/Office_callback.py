from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.utils.media_group import MediaGroupBuilder


async def answer_Office(call: types.CallbackQuery):
    def get_keyboard():
        keyboard = InlineKeyboardBuilder()
        keyboard.button(text='Room', callback_data='office_room')
        keyboard.button(text='Iceberg', callback_data='office_iceberg')
        keyboard.adjust(2)
        return keyboard.as_markup()

    photos_Office = MediaGroupBuilder()
    photos_Office.add(
        type='photo',
        caption='Room',
        media='https://deledzavod.ru/katalog/osveshhenie-dlya-ofisov/room-k-18/'
    )
    photos_Office.add(
        type='photo',
        caption='Iceberg',
        media='https://deledzavod.ru/katalog/proizvodstvennoe-osveshenie/iiceberg2-30/'
    )
    await call.message.answer_media_group(media=photos_Office.build())
    await call.message.answer('Выберите тип светильников:', reply_markup=get_keyboard())
    await call.answer()
