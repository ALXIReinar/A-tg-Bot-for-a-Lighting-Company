from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.utils.media_group import MediaGroupBuilder


async def answer_promishl(call: types.CallbackQuery):
    def keyboard_build():
        keyboard = InlineKeyboardBuilder()
        keyboard.button(text='Long-P', callback_data='promishl_long-p')
        keyboard.button(text='Optimus-P', callback_data='promishl_optimus-p')
        keyboard.button(text='Optimis-P-Lite', callback_data='promishl_optimus-p-lite')
        keyboard.button(text='Iceberg', callback_data='promishl_iceberg')
        keyboard.button(text='Omega-P', callback_data='promishl_omega-p')
        keyboard.button(text='Перейти на сайт', url='https://deledzavod.ru/katalog/')   # КНОПКА-ССЫЛКА "ПЕРЕЙТИ НА САЙТ"
        keyboard.adjust(2, 3, 1)
        return keyboard.as_markup()

    media = MediaGroupBuilder()
    media.add(
        type='photo',
        caption='Long-P',
        media='https://deledzavod.ru/wp-content/uploads/2021/11/long-p-600-1-1.png'
    )
    media.add(
        type='photo',
        caption='Optimus-P',
        media='https://deledzavod.ru/wp-content/uploads/2021/06/optimus-r550-4-1.png'
    )
    media.add(
        type='photo',
        caption='Optimus-P-Lite',
        media='https://sun9-39.userapi.com/impg/-qyJ0ooulAcKQ0Ogjzbu_da7u8mMhvvUceMf_g/uWqCqBY3H9Y.jpg?size=2560x1517&quality=96&sign=ff8af967a5bfea07a0bb44ad5c209d47&type=album'
    )
    media.add(
         type='photo',
         caption='Iceberg',
         media='https://deledzavod.ru/wp-content/uploads/2021/11/iceberg-1-1.png'
    )
    media.add(
        type='photo',
        caption='Omega-P',
        media='https://sun9-36.userapi.com/impg/8QMbmNzmczmUGO8OFOVvK7CAOyV4Ox0Wo0cVmw/V7v6z8n_O9s.jpg?size=1607x1000&quality=96&sign=0ad0425299cc52071a94eecc1bedf29e&type=album'
    )

    await call.message.answer_media_group(media=media.build())
    await call.message.answer('Выберите тип светильника:', reply_markup=keyboard_build())
    await call.answer()
