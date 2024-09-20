from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder


async def answer_AZS(call: types.CallbackQuery):
    def get_keyboard():
        keyboard = InlineKeyboardBuilder()
        keyboard.button(text='Optimus-FS', callback_data='azs_optimus-fs')
        keyboard.adjust(1)
        return keyboard.as_markup()
    await call.message.answer_photo(photo='https://sun9-38.userapi.com/impg/vvfsNSSc4mY9j496r6k6G7Drtr_ZSBNZSDV-ew/ccmQ7LZlX-I.jpg?size=1920x659&quality=96&sign=15dc66d58e56726ff9162efbdc51e6b5&type=album',
                                    caption='Выберите тип светильника',
                                    reply_markup=get_keyboard())
    await call.answer()