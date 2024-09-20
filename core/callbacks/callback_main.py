from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from core.callbacks.callbacks_2lvl.Promishl_callback import answer_promishl
from core.callbacks.callbacks_2lvl.AZS_callback import answer_AZS
from core.callbacks.callbacks_2lvl.Street_callback import answer_Street
from core.callbacks.callbacks_2lvl.ZHKH_callback import answer_ZHKH
from core.callbacks.callbacks_2lvl.SellSquare_callback import answer_SellSquare
from core.callbacks.callbacks_2lvl.Explosion_callback import answer_Explosion
from core.callbacks.callbacks_2lvl.Office_callback import answer_Office
from core.callbacks.callbacks_2lvl.Park_callback import answer_Park
from core.callbacks.callbacks_2lvl.Architecture_callback import answer_Architecture
from core.callbacks.callbacks_3_4lvl.answer_type_lamp import answer_by_type_lamp, answer_by_type_lamp_next, answer_by_type_lamp_previous
from core.callbacks.callbacks_3_4lvl.answer_by_lamp_name import answer_by_lamp_name
from core.callbacks.utils.state_machine import SaveSteps

from core.data.SQLite_block import db
from core.for_devs import search_result


async def answer_by_menu(call: CallbackQuery, state: FSMContext):
    """ Ветвь 1лвл """
    if call.data == 'Promishl':
        await answer_promishl(call)
    elif call.data == 'AZS':
        await answer_AZS(call)
    elif call.data == 'Street':
        await answer_Street(call)
    elif call.data == 'ZHKH':
        await answer_ZHKH(call)
    elif call.data == 'SellSquare':
        await answer_SellSquare(call)
    elif call.data == 'Explosion':
        await answer_Explosion(call)
    elif call.data == 'Office':
        await answer_Office(call)
    elif call.data == 'Park':
        await answer_Park(call)
    elif call.data == 'Architecture':
        await answer_Architecture(call)

    elif db.category_exists(call.data):         # Ветвь 3лвл
        await answer_by_type_lamp(call, state)
    elif call.data == 'next':
        await answer_by_type_lamp_next(call, state)
    elif call.data == 'previous':
        await answer_by_type_lamp_previous(call, state)

    elif db.get_lamp(call.data):                # Ветвь 2-3лвл
        await answer_by_lamp_name(call)

    elif call.data == 'more':                   # коллбек по кнопке "показать ещё" в  поиске светильника
        context_data = await state.get_data()
        current_search = context_data.get('current_search')
        message = context_data.get('message')
        await state.update_data(search_name=message.text, more=current_search)
        await state.set_state(SaveSteps.GET_SEARCH)
        await search_result(message, state)
        await call.answer()

    else:
        await call.answer()
