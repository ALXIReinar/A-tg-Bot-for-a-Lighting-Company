from aiogram.types import CallbackQuery

from core.data.SQLite_block import db
from core.callbacks.utils.keyboards import get_keyboard_4lvl_branch


async def answer_by_lamp_name(call: CallbackQuery):
    res = db.get_lamp(call.data)
    text = f'''<b><code>{res[0][1]}</code></b>
    
               Мощность - {res[0][2]} W
    
               Стоимость - {res[0][3]}₽
               
               Ссылка - {res[0][4]}
    '''
    await call.message.answer(text, reply_markup=get_keyboard_4lvl_branch(res[0][4]))
    await call.answer()
