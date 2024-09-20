from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.utils.media_group import MediaGroupBuilder


async def answer_Park(call: types.CallbackQuery):
    def get_keyboard():
        keyboard = InlineKeyboardBuilder()
        keyboard.button(text='Brum-S1', callback_data='park_brum-s1')
        keyboard.button(text='Brum-S2', callback_data='park_brum-s2')
        keyboard.button(text='Brum-S3', callback_data='park_brum-s3')
        keyboard.button(text='Brum-S4', callback_data='park_brum-s4')
        keyboard.button(text='Brum-Cup', callback_data='park_brum-cup')
        keyboard.button(text='Brum-C', callback_data='park_brum-c')
        keyboard.button(text='Brum-RL', callback_data='park_brum-rl')
        keyboard.button(text='Brum-PL', callback_data='park_brum-pl')
        keyboard.button(text='Brum-L', callback_data='park_brum-l')
        keyboard.button(text='Brum Ring', callback_data='park_brum-ring')
        keyboard.button(text='Brum Quadro', callback_data='park_brum-quadro')
        keyboard.button(text='Brum-Elegant', callback_data='park_brum-elegant')
        keyboard.button(text='Tub-R1', callback_data='park_tub-r1')
        keyboard.button(text='Tub-R2', callback_data='park_tub-r2')
        keyboard.button(text='Low', callback_data='park_low')
        keyboard.button(text='Prima', callback_data='park_prima')
        keyboard.button(text='Beta', callback_data='park_beta')
        keyboard.button(text='Beta Neo', callback_data='park_beta-neo')
        keyboard.adjust(4, 4, 4, 4, 2)
        return keyboard.as_markup()

    photos_Park1 = MediaGroupBuilder()
    photos_Park1.add(
        type='photo',
        caption='Brum-S1',
        media='https://deledzavod.ru/katalog/parkovoe-osveshhenie/brum-s1-quattro-40/'
    )
    photos_Park1.add(
        type='photo',
        caption='Brum-S2',
        media='https://deledzavod.ru/katalog/parkovoe-osveshhenie/brum-s2-quattro/'
    )
    photos_Park1.add(
        type='photo',
        caption='Brum-S3',
        media='https://deledzavod.ru/katalog/parkovoe-osveshhenie/brum-s3-quattro/'
    )
    photos_Park1.add(
        type='photo',
        caption='Brum-S4',
        media='https://deledzavod.ru/katalog/parkovoe-osveshhenie/brum-s4-quattro-80/'
    )
    photos_Park1.add(
        type='photo',
        caption='Brum-Cup',
        media='https://deledzavod.ru/katalog/parkovoe-osveshhenie/brum-cup-40/'
    )
    photos_Park1.add(
        type='photo',
        caption='Brum-C',
        media='https://deledzavod.ru/katalog/parkovoe-osveshhenie/brum-c-60/'
    )
    photos_Park1.add(
        type='photo',
        caption='Brum-RL',
        media='https://deledzavod.ru/katalog/parkovoe-osveshhenie/brum-rl-50l3m/'
    )
    photos_Park1.add(
        type='photo',
        caption='Brum-PL',
        media='https://deledzavod.ru/katalog/parkovoe-osveshhenie/brum-pl2-50/'
    )
    photos_Park1.add(
        type='photo',
        caption='Brum-L',
        media='https://deledzavod.ru/katalog/parkovoe-osveshhenie/brum-l-25/'
    )
    photos_Park2 = MediaGroupBuilder()
    photos_Park2.add(
        type='photo',
        caption='Brum Ring',
        media='https://deledzavod.ru/katalog/parkovoe-osveshhenie/beta-ring-quattro-25/'
    )
    photos_Park2.add(
        type='photo',
        caption='Brum Quadro',
        media='https://deledzavod.ru/katalog/parkovoe-osveshhenie/brum-quadro-1-l1000/'
    )
    photos_Park2.add(
        type='photo',
        caption='Brum-Elegant',
        media='https://deledzavod.ru/katalog/parkovoe-osveshhenie/brum-elegant-60l5/'
    )
    photos_Park2.add(
        type='photo',
        caption='Tub-R1',
        media='https://deledzavod.ru/katalog/parkovoe-osveshhenie/tub-r1-20-l1000-300/'
    )
    photos_Park2.add(
        type='photo',
        caption='Tub-R2',
        media='https://deledzavod.ru/katalog/parkovoe-osveshhenie/tub-r2-20-40-l1000-300/'
    )
    photos_Park2.add(
        type='photo',
        caption='Low',
        media='https://deledzavod.ru/katalog/parkovoe-osveshhenie/low-r10/'
    )
    photos_Park2.add(
        type='photo',
        caption='Prima',
        media='https://deledzavod.ru/katalog/parkovoe-osveshhenie/prima-quinto/'
    )
    photos_Park2.add(
        type='photo',
        caption='Beta',
        media='https://deledzavod.ru/katalog/parkovoe-osveshhenie/beta-80/'
    )
    photos_Park2.add(
        type='photo',
        caption='Beta Neo',
        media='https://deledzavod.ru/katalog/parkovoe-osveshhenie/beta-neo-60/'
    )

    await call.message.answer_media_group(media=photos_Park1.build())
    await call.message.answer_media_group(media=photos_Park2.build())
    await call.message.answer('Выберите тип светильников:', reply_markup=get_keyboard())
    await call.answer()
