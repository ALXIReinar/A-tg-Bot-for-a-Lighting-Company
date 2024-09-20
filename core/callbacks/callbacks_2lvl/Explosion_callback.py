from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.utils.media_group import MediaGroupBuilder


async def answer_Explosion(call: types.CallbackQuery):
    def get_keyboard():
        keyboard = InlineKeyboardBuilder()
        keyboard.button(text='Optimus-Ex1-P', callback_data='boom_optimus-exp1')
        keyboard.button(text='Optimus-Ex-P', callback_data='boom_optimus-exp')
        keyboard.button(text='Long-Ex1-P', callback_data='boom_long-exp1')
        keyboard.button(text='Long-Ex-P', callback_data='boom_long-exp')
        keyboard.button(text='Omega-1ExD', callback_data='boom_omega-exp')
        keyboard.adjust(3, 2)
        return keyboard.as_markup()

    photos_Explosion = MediaGroupBuilder()
    photos_Explosion.add(
        type='photo',
        caption='OPTIMUS-1Ex-P',
        media='https://deledzavod.ru/katalog/vzryvozashhishhennye-svetilniki/optimus-ex-p/optimus-ex-p-10/'
    )
    photos_Explosion.add(
        type='photo',
        caption='OPTIMUS-Ex-P',
        media='https://deledzavod.ru/katalog/vzryvozashhishhennye-svetilniki/optimus-ex-p/optimus-ex-p-10/'
    )
    photos_Explosion.add(
        type='photo',
        caption='LONG-1Ex-P',
        media='https://deledzavod.ru/katalog/vzryvozashhishhennye-svetilniki/long-1ex-p-10-l03-optic/'
    )
    photos_Explosion.add(
        type='photo',
        caption='LONG-Ex-P',
        media='https://deledzavod.ru/katalog/vzryvozashhishhennye-svetilniki/long-ex-p-10-l03/'
    )
    photos_Explosion.add(
        type='photo',
        caption='OMEGA-1ExD',
        media='https://deledzavod.ru/katalog/vzryvozashhishhennye-svetilniki/vzryvozashhishhennyj-svetilnik-omega-1exd-10/'
    )

    await call.message.answer_media_group(media=photos_Explosion.build())
    await call.message.answer('Выберите тип светильника:', reply_markup=get_keyboard())
    await call.answer()
