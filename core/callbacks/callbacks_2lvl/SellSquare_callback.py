from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder


async def answer_SellSquare(call: types.CallbackQuery):
    def get_keyboard():
        keyboard = InlineKeyboardBuilder()
        keyboard.button(text='Long-R', callback_data='SQuare_long-r')
        return keyboard.as_markup()

    await call.message.answer_photo(photo='https://deledzavod.ru/katalog/svetilniki-dlya-torgovyh-ploshhadej/long-r/cvetilnik-dlya-torgovyh-ploshhadej-long-r-20-l06/',
                                    caption='Выберите тип светильника:',
                                    reply_markup=get_keyboard())
    await call.answer()
