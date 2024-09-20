from core.data.SQLite_block import db
import re

from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest

from core.callbacks.utils.state_machine import SaveSteps
from core.callbacks.utils.keyboards import (get_keyboard_ADDLAMP_DELETE_EDIT_FORDEVS,
                                            get_keyboard_UPDATE_FORDEVS,
                                            get_quit,
                                            get_keyboard_1lvl_branch,
                                            get_keyboard_2lvl_branch,
                                            get_keyboard_CONFIRM,
                                            profile,
                                            add_attr,
                                            get_keyboard_SEARCH)
from core.callbacks.utils.subcategories import SubCategory, SubCategoryFormat

from core.config import PASSWORD


async def for_devs_(message: types.Message, state: FSMContext):
    await message.answer('!Вы открыли раздел для разработчиков!\n\n'
                         'Введите пароль, чтобы пройти верификацию',
                         reply_markup=types.ReplyKeyboardRemove(remove_keyboard=True))
    status = db.user_exists(message.from_user.id)[0][2]
    if status:
        await message.answer('Вы уже имеете доступ к дополнительному функционалу\n'
                             'Перезапустите бота, если команды не появились /start')
        await state.clear()
    else:
        await state.set_state(SaveSteps.GET_PASSWORD)

async def get_password(message: types.Message, state: FSMContext):
    if message.text == PASSWORD:
        db.add_dev(message.from_user.id)
        await message.answer('Верификация прошла успешно\nВведите команду /start и перезайдите в чат для обновления меню команд!')
    else:
        await message.answer('Пароль введён неверно!')
    await state.clear()



"""Декораторы"""
def DevCheck(func):
    async def wrapper(mes: types.Message, state: FSMContext):
        await state.set_state(SaveSteps.CHECK)
        info = db.user_exists(mes.from_user.id)
        status = info[0][2]
        if status:
            res = await func(mes, state)
            return res
        else:
            await mes.answer('Вам недоступна эта команда. Пройдите верификацию /for_devs')
            await state.clear()
    return wrapper
def CancelActivity(func):
    async def wrapper(mes: types.Message, state: FSMContext):
        if mes.text.lower() == 'отменить действие':
            await mes.answer('Действие отменено',
                             reply_markup=types.ReplyKeyboardRemove(remove_keyboard=True))
            await state.clear()
        else:
            result = await func(mes, state)
            return result
    return wrapper



"""/🤣add_lamp"""
@DevCheck
async def get_form(message: types.Message, state: FSMContext):
    await message.answer('!Добавление новой записи светильника!',
                         reply_markup=types.ReplyKeyboardRemove(remove_keyboard=True))
    await message.answer('Введите название светильника')
    await state.set_state(SaveSteps.GET_NAME)


@CancelActivity
async def get_name(message: types.Message, state: FSMContext):
    contex_data = await state.get_data()
    name = contex_data.get('name')

    await message.answer('Введите мощность светильника\n<b>Вводите только цифры</b>', reply_markup=get_quit())
    if name:
        pass
    else:
        await state.update_data(name=message.text)
    await state.set_state(SaveSteps.GET_VOLTAGE)

@CancelActivity
async def get_voltage(message: types.Message, state: FSMContext):
    try:
        int(message.text)
        await state.update_data(voltage=abs(int(message.text)))
        await state.set_state(SaveSteps.GET_LINK)
        await message.answer('Введите ссылку на светильник',
                             reply_markup=get_quit())
    except ValueError:
        await message.answer('Некорректный ввод')
        await get_name(message, state)

@CancelActivity
async def get_link(message: types.Message, state: FSMContext):
    contex_data = await state.get_data()
    link = contex_data.get('link')

    await message.answer('Введите стоимость светильника\n<b>Вводите только цифры</b>', reply_markup=get_quit())
    if link:
        pass
    else:
        await state.update_data(link=message.text)
    await state.set_state(SaveSteps.GET_COST)

@CancelActivity
async def get_cost(message: types.Message, state: FSMContext):
    contex_data = await state.get_data()
    cost = contex_data.get('cost')

    if cost:
        await message.answer('Выберите категорию светильника', reply_markup=get_keyboard_1lvl_branch())
        await state.set_state(SaveSteps.GET_CATEGORY_1LVL)
    else:
        try:
            int(message.text.lower())
            await message.answer('Выберите категорию светильника', reply_markup=get_keyboard_1lvl_branch())
            await state.update_data(cost=abs(int(message.text)))
            await state.set_state(SaveSteps.GET_CATEGORY_1LVL)
        except ValueError:
            await message.answer('Некорректный ввод')
            await get_link(message, state)

async def get_category_1lvl(message: types.Message, state: FSMContext):
    if SubCategory.get(message.text):
        await message.answer('Выберите подкатегорию:', reply_markup=get_keyboard_2lvl_branch(message.text))
        await state.update_data(category_1lvl=message.text)
        await state.set_state(SaveSteps.GET_CATEGORY_2LVL)
    else:
        await message.answer('Выберите подкатегорию из указанных на кнопке!')
        await get_cost(message, state)

async def get_category_2lvl(message: types.Message, state: FSMContext):
    await state.update_data(category_2lvl=message.text)
    context_data = await state.get_data()
    await state.update_data(category=context_data.get('category_1lvl') + '_' + context_data.get('category_2lvl'))

    context_data = await state.get_data()
    is_update = context_data.get('update')
    name = context_data.get('name')
    voltage = context_data.get('voltage')
    cost = context_data.get('cost')
    link = context_data.get('link')
    category = context_data.get('category')

    await message.answer(f'Данные для нового светильника:\n\n'
                         f'Название - <code>{name}</code>\n'
                         f'Мощность - {voltage} W(Вт)\n'
                         f'Ссылка - {link}\n'
                         f'Стоимость - {cost}₽\n'
                         f'Категория - {category}\n\n'
                         f'Продолжить с такими данными?', reply_markup=get_keyboard_ADDLAMP_DELETE_EDIT_FORDEVS())

    if is_update:
        await state.set_state(SaveSteps.GET_UPDATE)
    else:
        await state.set_state(SaveSteps.GET_ACTIVITY)

async def get_activity(message: types.Message, state: FSMContext):
    context_data = await state.get_data()
    name = context_data.get('name')
    voltage = context_data.get('voltage')
    cost = context_data.get('cost')
    link = context_data.get('link')
    category = context_data.get('category')


    if message.text.lower() == 'да':

        check = db.lamp_exists(name)
        if check:
            await message.answer(f'Светильник с таким именем уже существует:\n{name}',
                                 reply_markup=types.ReplyKeyboardRemove(remove_keyboard=True))
            await state.clear()
        else:
            db.add_lamp(name, voltage, cost, link, category)
            await message.answer(f'Светильник успешно добавлен в базу данных!',
                                 reply_markup=types.ReplyKeyboardRemove(remove_keyboard=True))
            await state.clear()

    elif message.text.lower() == 'редактировать внесённые данные':

        await get_form(message, state)

    elif message.text.lower() == 'отменить действие':

        await message.answer('Действие отменено',
                             reply_markup=types.ReplyKeyboardRemove(remove_keyboard=True))
        await state.clear()

    else:
        await message.answer('Неизвестная команда. Действие отменено',
                             reply_markup=types.ReplyKeyboardRemove(remove_keyboard=True))
        await state.clear()



"""edit"""
async def get_name_edit(message: types.Message, state: FSMContext):
    context_data = await state.get_data()
    source = context_data.get('source')
    if source:
        await message.answer('Введите новое название светильника',
                             reply_markup=types.ReplyKeyboardRemove(remove_keyboard=True))
        await state.set_state(SaveSteps.EDIT_NAME)
    else:
        if message.text.lower() == 'название':
            await message.answer('Введите новое название светильника',
                                 reply_markup=types.ReplyKeyboardRemove(remove_keyboard=True))
            await state.update_data(source='get_name_edit')
            await state.set_state(SaveSteps.EDIT_NAME)

async def edit_name(message: types.Message, state: FSMContext):
    await state.update_data(edit=message.text)
    context_data = await state.get_data()
    name = context_data.get('edit')
    await message.answer(f'Изменённый параметр:\nНазвание - <code>{name}</code>\n\nПринять изменения?',
                         reply_markup=get_keyboard_ADDLAMP_DELETE_EDIT_FORDEVS())
    await state.set_state(SaveSteps.GET_CONFIRM_EDITS)

async def get_voltage_edit(message: types.Message, state: FSMContext):
    context_data = await state.get_data()
    source = context_data.get('source')
    if source:
        await message.answer('Введите новую мощность светильника',
                             reply_markup=types.ReplyKeyboardRemove(remove_keyboard=True))
        await state.set_state(SaveSteps.EDIT_VOLTAGE)
    else:
        if message.text.lower() == 'мощность':
            await message.answer('Введите новую мощность светильника',
                                 reply_markup=types.ReplyKeyboardRemove(remove_keyboard=True))
            await state.update_data(source='get_voltage_edit')
            await state.set_state(SaveSteps.EDIT_VOLTAGE)

async def edit_voltage(message: types.Message, state: FSMContext):
    try:
        int(message.text)
        await state.update_data(edit=abs(int(message.text)))
        context_data = await state.get_data()
        voltage = context_data.get('edit')
        await message.answer(f'Изменённый параметр:\nМощность: {voltage}W\n\nПринять изменения?',
                             reply_markup=get_keyboard_ADDLAMP_DELETE_EDIT_FORDEVS())
        await state.set_state(SaveSteps.GET_CONFIRM_EDITS)
    except ValueError:
        await message.answer("Некорректный ввод. Попробуйте снова")
        await state.set_state(SaveSteps.GET_VOLTAGE_EDIT)
        await get_voltage_edit(message, state)

async def get_cost_edit(message: types.Message, state: FSMContext):
    context_data = await state.get_data()
    source = context_data.get('source')
    if source:
        await message.answer('Введите другую стоимость светильника',
                             reply_markup=types.ReplyKeyboardRemove(remove_keyboard=True))
        await state.set_state(SaveSteps.EDIT_COST)
    else:
        if message.text.lower() == 'стоимость':
            await message.answer('Введите другую стоимость светильника',
                                 reply_markup=types.ReplyKeyboardRemove(remove_keyboard=True))
            await state.update_data(source='get_cost_edit')
            await state.set_state(SaveSteps.EDIT_COST)

async def edit_cost(message: types.Message, state: FSMContext):
    try:
        int(message.text)
        await state.update_data(edit=abs(int(message.text)))
        context_data = await state.get_data()
        cost = context_data.get('edit')
        await message.answer(f'Изменённый параметр:\nСтоимость - {cost}₽\n\nПринять изменения?',
                             reply_markup=get_keyboard_ADDLAMP_DELETE_EDIT_FORDEVS())
        await state.set_state(SaveSteps.GET_CONFIRM_EDITS)
    except ValueError:
        await message.answer("Некорректный ввод. Попробуйте снова")
        await state.set_state(SaveSteps.GET_VOLTAGE_EDIT)
        await get_voltage_edit(message, state)
async def get_link_edit(message: types.Message, state: FSMContext):
    context_data = await state.get_data()
    source = context_data.get('source')
    if source:
        await message.answer('Введите новую ссылку на светильник',
                             reply_markup=types.ReplyKeyboardRemove(remove_keyboard=True))
        await state.set_state(SaveSteps.EDIT_LINK)
    else:
        if message.text.lower() == 'ссылка':
            await message.answer('Введите новую ссылку на светильник',
                                 reply_markup=types.ReplyKeyboardRemove(remove_keyboard=True))
            await state.update_data(source='get_link_edit')
            await state.set_state(SaveSteps.EDIT_LINK)

async def edit_link(message: types.Message, state: FSMContext):
    await state.update_data(edit=message.text)
    context_data = await state.get_data()
    link = context_data.get('edit')
    await message.answer(f'Изменённый параметр:\nСсылка: {link}\n\nПринять изменения?',
                         reply_markup=get_keyboard_ADDLAMP_DELETE_EDIT_FORDEVS())
    await state.set_state(SaveSteps.GET_CONFIRM_EDITS)

async def get_category_edit(message: types.Message, state: FSMContext):
    context_data = await state.get_data()
    source = context_data.get('source')
    if source:
        await message.answer('Выберите категорию:', reply_markup=get_keyboard_1lvl_branch())
        await state.set_state(SaveSteps.GET_CATEGORY_LITE1)
    else:
        if message.text.lower() == 'категория':
            await message.answer('Выберите категорию:', reply_markup=get_keyboard_1lvl_branch())
            await state.update_data(source='get_category_edit')
            await state.set_state(SaveSteps.GET_CATEGORY_LITE1)

        else:
            await message.answer('Выберите категорию из указанных на кнопке!')
            await get_category_edit(message, state)
async def get_category_LITE1(message: types.Message, state: FSMContext):
    if SubCategory.get(message.text):
        await message.answer('Выберите подкатегорию:', reply_markup=get_keyboard_2lvl_branch(message.text))
        await state.update_data(category_lite1=message.text)
        await state.set_state(SaveSteps.GET_CATEGORY_LITE2)
    else:
        await message.answer('Выберите подкатегорию из указанных на кнопке!')
        await get_category_edit(message, state)
async def get_category_LITE2(message: types.Message, state: FSMContext):
    await state.update_data(category_lite2=message.text)
    context_data = await state.get_data()
    await state.update_data(edit=context_data.get('category_lite1') + '_' + context_data.get('category_lite2'))
    context_data = await state.get_data()
    category = context_data.get('edit')

    text = f'Изменённый параметр:\nКатегория - {category}\n\nПринять изменения?'
    await message.answer(text, reply_markup=get_keyboard_ADDLAMP_DELETE_EDIT_FORDEVS())
    await state.set_state(SaveSteps.GET_CONFIRM_EDITS)


'''edit_head'''
async def get_confirm_edits(message: types.Message, state: FSMContext):
    if message.text.lower() == 'да':

        context_data = await state.get_data()
        param = context_data.get('edit')
        column = context_data.get('column')
        name = context_data.get('old_name')
        db.update_attr(column, param, name)
        await message.answer(f'Данные успешно изменены!', reply_markup=types.ReplyKeyboardRemove(remove_keyboard=True))
        await state.clear()

    elif message.text.lower() == 'редактировать внесённые данные':

        context_data = await state.get_data()
        functions = {
            'get_name_edit': get_name_edit,
            'get_voltage_edit': get_voltage_edit,
            'get_cost_edit': get_cost_edit,
            'get_link_edit': get_link_edit,
            'get_category_edit': get_category_edit
        }
        func = functions[context_data.get('source')]
        await func(message, state)

    elif message.text.lower() == 'отменить действие':

        await message.answer('Действие отменено',
                             reply_markup=types.ReplyKeyboardRemove(remove_keyboard=True))
        await state.clear()

    else:
        await message.answer('Неизвестная команда. Действие отменено',
                             reply_markup=types.ReplyKeyboardRemove(remove_keyboard=True))
        await state.clear()


"""/search"""
async def search_lamp(message: types.Message, state: FSMContext):
    await message.answer('!Поиск светильника в базе данных!')
    await state.clear()
    await message.answer('Введите <u><i>частичное/полное</i></u> название светильника\nСм. /search_help',
                         reply_markup=get_quit())
    await state.set_state(SaveSteps.GET_SEARCH)

@CancelActivity
async def search_result(message: types.Message, state: FSMContext):
    await state.update_data(search_name=message.text)
    context_data = await state.get_data()
    search_name = context_data.get('search_name')

    request = ""
    for char in range(len(search_name)):
        if re.match(r'[a-zA-Z]', search_name[char]):
            request += search_name[char].upper()

    search = search_name
    if 2 < len(request) < 5:
        search = request

    more = context_data.get('current_search')
    if more:
        current = more
    else:
        current = 1
    res = await db.search_lamp(search, current, search)

    if bool(len(res[0])):
        text = ''
        search_info = res[0]
        last = res[1]
        for i in range(len(search_info)):
            text += (f'\n<b>ID - {search_info[i][0]}</b>\n'
                     f'      Название - <code>{search_info[i][1]}</code>\n'
                     f'      Мощность - {search_info[i][2]} W | Вт\n'
                     f'      Стоимость - {search_info[i][3]}₽\n'
                     f'      Ссылка - {search_info[i][4]}\n')
            category = search_info[i][5]
            category_lvl2 = category.split('_')[0]
            category_lvl3 = category.split('_')[1]
            category = SubCategoryFormat[category_lvl2] + ' --> ' + category_lvl3
            text += f'      Категория - {category}'

        await message.answer(text, reply_markup=get_keyboard_SEARCH(last))
    else:
        await message.answer(f'Светильники с именем `{message.text}` не найдены/были полностью показаны')
    await state.clear()
    await state.update_data(current_search=current + 1, message=message)


"""/delete_lamp"""
@DevCheck
async def delete_lamp(message: types.Message, state: FSMContext):
    await message.answer('!Удаление светильника!', reply_markup=types.ReplyKeyboardRemove(remove_keyboard=True))
    await message.answer('Введите <b>полное</b> название светильника')
    await state.set_state(SaveSteps.GET_DELETE)

async def delete_res(message: types.Message, state: FSMContext):
    await state.update_data(name_delete=message.text)
    context_data = await state.get_data()
    name = context_data.get('name_delete')
    next_step = db.lamp_exists(name)

    if next_step:
        res = db.get_lamp(name)
        await message.answer(f'ID - {res[0][0]}\n'
                             f'Название - <code>{res[0][1]}</code>\n'
                             f'Мощность - {res[0][2]} W\n'
                             f'Стоимость - {res[0][3]}₽\n'
                             f'Ссылка - {res[0][4]}\n'
                             f'Категория - {res[0][5]}\n\n'
                             f'Удалить данную запись?', reply_markup=get_keyboard_ADDLAMP_DELETE_EDIT_FORDEVS())
        await state.set_state(SaveSteps.GET_ACTIVITY_DELETE)

    else:
        await message.answer('Светильник не найден')
        await state.clear()

async def get_activity_delete(message: types.Message, state: FSMContext):
    if message.text.lower() == 'да':

        await message.answer('Вы уверены?', reply_markup=get_keyboard_CONFIRM())
        await state.set_state(SaveSteps.GET_CONFIRM)

    elif message.text.lower() == 'редактировать внесённые данные':

        await delete_lamp(message, state)

    elif message.text.lower() == 'отменить действие':

        await message.answer('Действие отменено',
                             reply_markup=types.ReplyKeyboardRemove(remove_keyboard=True))
        await state.clear()

    else:
        await message.answer('Неизвестная команда. Действие отменено',
                             reply_markup=types.ReplyKeyboardRemove(remove_keyboard=True))
        await state.clear()

async def get_confirmation(message: types.Message, state: FSMContext):
    if message.text.lower() == 'подтвердить':
        context_data = await state.get_data()
        name = context_data.get('name_delete')

        db.lamp_delete(name)
        await message.answer('Запись о светильнике успешно удалена!',
                             reply_markup=types.ReplyKeyboardRemove(remove_keyboard=True))

    elif message.text.lower() == 'отмена':
        await message.answer('Действие отменено', reply_markup=types.ReplyKeyboardRemove(remove_keyboard=True))

    else:
        await message.answer('Неизвестная команда. Действие отменено',
                             reply_markup=types.ReplyKeyboardRemove(remove_keyboard=True))

    await state.clear()



"""/update_lamp"""
@DevCheck
async def get_update_lamp(message: types.Message, state: FSMContext):
    await message.answer('!Обновление данных записи о светильнике!',
                         reply_markup=types.ReplyKeyboardRemove(remove_keyboard=True))
    await message.answer('Введите <b>полное</b> название светильника')
    await state.set_state(SaveSteps.SEARCH_NAME)

@CancelActivity
async def search_name(message: types.Message, state: FSMContext):
    if db.lamp_exists(message.text):
        res = db.get_lamp(message.text)
        await message.answer('Запись о светильнике найдена:\n\n'
                             f'ID - {res[0][0]}\n'
                             f'Название - <code>{res[0][1]}</code>\n'
                             f'Мощность - {res[0][2]} W\n'
                             f'Стоимость - {res[0][3]}₽\n'
                             f'Ссылка - {res[0][4]}\n'
                             f'Категория - {res[0][5]}\n\n'
                             f'Перейти к изменению записи о светильнике?', reply_markup=get_keyboard_UPDATE_FORDEVS())
        await state.update_data(old_name=res[0][1])
        await state.set_state(SaveSteps.GET_NEW_NAME)
    else:
        await message.answer('Запись о светильнике не найдена!\n'
                             'Получите данные о записи через команду /search',
                             reply_markup=types.ReplyKeyboardRemove(remove_keyboard=True))
        await state.clear()

"""Апдейт одного параметра"""
async def get_edit(message: types.Message, state: FSMContext):
    await message.answer('!Изменение параметра!', reply_markup=add_attr())
    await state.set_state(SaveSteps.EDIT_ATTR)
async def edit_attr(message: types.Message, state: FSMContext):
    states_funcs = {
        "название": (get_name_edit, SaveSteps.GET_NAME_EDIT),
        "мощность": (get_voltage_edit, SaveSteps.GET_VOLTAGE_EDIT),
        "стоимость": (get_cost_edit, SaveSteps.GET_COST_EDIT),
        "ссылка": (get_link_edit, SaveSteps.GET_LINK_EDIT),
        "категория": (get_category_edit, SaveSteps.GET_PRED_EDIT)
    }
    columns = {
        "название": 'name',
        "мощность": 'voltage',
        "стоимость": 'cost',
        "ссылка": 'link',
        "категория": 'category'
    }
    mes = message.text.lower()
    if mes in columns.keys():
        for attr in columns.keys():
            if attr == mes:
                await state.update_data(column=columns[mes])
                func = states_funcs[mes][0]
                state_name = states_funcs[mes][1]
                await state.set_state(state_name)
                await func(message, state)

    else:
        await message.answer('Неизвестный параметр\nДействие отменено')
        await state.clear()



async def get_new_name(message: types.Message, state: FSMContext):
    if message.text.lower() == 'да':

        await message.answer('Введите новое название светильника',
                             reply_markup=types.ReplyKeyboardRemove(remove_keyboard=True))
        await state.update_data(update='1')
        await state.set_state(SaveSteps.GET_NEW_NAME2)

    elif message.text.lower() == 'изменить один параметр':

        await get_edit(message, state)

    elif message.text.lower() == 'отменить действие':

        await message.answer('Действие отменено',
                             reply_markup=types.ReplyKeyboardRemove(remove_keyboard=True))
        await state.clear()

    else:
        await message.answer('Неизвестная команда. Действие отменено',
                             reply_markup=types.ReplyKeyboardRemove(remove_keyboard=True))
        await state.clear()

async def get_activity_update(message: types.Message, state: FSMContext):
    context_data = await state.get_data()
    name = context_data.get('name')
    voltage = context_data.get('voltage')
    cost = context_data.get('cost')
    link = context_data.get('link')
    category = context_data.get('category')
    old_name = context_data.get('old_name')


    if message.text.lower() == 'да':
        db.update_lamp(name, voltage, cost, link, category, old_name)
        await message.answer('Запись о светильнике успешно обновлена!',
                             reply_markup=types.ReplyKeyboardRemove(remove_keyboard=True))
        await state.clear()

    elif message.text.lower() == 'редактировать внесённые данные':

        await get_update_lamp(message, state)

    elif message.text.lower() == 'отменить действие':

        await message.answer('Действие отменено',
                             reply_markup=types.ReplyKeyboardRemove(remove_keyboard=True))
        await state.clear()

    else:
        await message.answer('Неизвестная команда. Действие отменено',
                             reply_markup=types.ReplyKeyboardRemove(remove_keyboard=True))
        await state.clear()


"""/id"""
async def show_id(message: types.Message):
    await message.answer(f'Ваш id:\n'
                         f'<code>{message.from_user.id}</code>')


'''/profile'''
@DevCheck
async def show_profile(message: types.Message, state: FSMContext):
    await message.answer('Введите id пользователя\nВводите только цифры')
    await state.set_state(SaveSteps.GET_ID)

async def answer_profile(message: types.Message, state: FSMContext):
    try:
        int(message.text)
        id = abs(int(message.text))
        await message.answer(f"Профиль пользователя:", reply_markup=profile(str(id)))

    except ValueError:
        await message.answer('Неверный id')
    except TelegramBadRequest:
        await message.answer('Неверный id')

    await state.clear()
