from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from core.callbacks.utils.keyboards import get_keyboard_3lvl_branch


async def answer_by_type_lamp(call: CallbackQuery, state: FSMContext):
    await state.update_data(subcategory=call.data)
    await call.message.answer('Выберите светильник:', reply_markup=await get_keyboard_3lvl_branch(state))
    await call.answer()


async def answer_by_type_lamp_next(call: CallbackQuery, state: FSMContext):
    context_data = await state.get_data()
    current = context_data.get('current_page')

    await call.message.edit_text('Выберите светильник:',
                                 reply_markup=await get_keyboard_3lvl_branch(state, current + 1))


async def answer_by_type_lamp_previous(call: CallbackQuery, state: FSMContext):
    context_data = await state.get_data()
    current = context_data.get('current_page')

    await call.message.edit_text('Выберите светильник:',
                                 reply_markup=await get_keyboard_3lvl_branch(state, current - 1))
