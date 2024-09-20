from aiogram import types
from aiogram.utils.media_group import MediaGroupBuilder
from aiogram.utils.keyboard import InlineKeyboardBuilder


async def answer_ZHKH(call: types.CallbackQuery):
    def get_keyboard():
        keyboard = InlineKeyboardBuilder()
        keyboard.button(text='FLAT-220V', callback_data='ZHKH_flat-220v')
        keyboard.button(text='FLAT-12-36V (Низковольтные)', callback_data='ZHKH_flat-12-36v')
        keyboard.button(text='FLAT-EM (Аварийные)', callback_data='ZHKH_flat-em')
        keyboard.adjust()
        return keyboard.as_markup()

    photos_ZHKH = MediaGroupBuilder()
    photos_ZHKH.add(
        type='photo',
        media='https://deledzavod.ru/katalog/osveshhenie-dlya-zhkh/flat-3/',
        caption='FLAT-220V'
    )
    photos_ZHKH.add(
        type='photo',
        media='https://deledzavod.ru/katalog/osveshhenie-dlya-zhkh/flat-3/',
        caption='FLAT-12-36V (Низковольтные)'
    )
    photos_ZHKH.add(
        type='photo',
        media='https://deledzavod.ru/katalog/osveshhenie-dlya-zhkh/flat-3/',
        caption='FLAT-EM (Аварийные)'
    )

    await call.message.answer_media_group(media=photos_ZHKH.build())
    await call.message.answer('Выберите тип светильника:', reply_markup=get_keyboard())
    await call.answer()
