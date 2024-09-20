import asyncio
from aiogram.filters import Command
from core.subcore import dp, bot, start, menu, website, user_help, dev_help, search_help, users
from core.callbacks.callback_main import answer_by_menu

import for_devs
from core.callbacks.utils.state_machine import SaveSteps


async def main():
    """Команды для пользователя"""
    dp.message.register(start, Command(commands='start'))
    dp.message.register(menu, Command(commands='menu'))
    dp.message.register(for_devs.search_lamp, Command(commands='search'))
    dp.message.register(for_devs.search_result, SaveSteps.GET_SEARCH)
    dp.message.register(search_help, Command(commands='search_help'))
    dp.message.register(website, Command(commands='website'))
    dp.message.register(user_help, Command(commands='help'))
    dp.message.register(for_devs.for_devs_, Command(commands='for_devs'))
    dp.message.register(for_devs.get_password, SaveSteps.GET_PASSWORD)

    dp.message.register(for_devs.DevCheck, SaveSteps.CHECK)

    """Команды Для разработчиков и /поиск"""
    dp.message.register(for_devs.get_form, Command(commands='add_lamp'))
    dp.message.register(for_devs.get_name, SaveSteps.GET_NAME)
    dp.message.register(for_devs.get_name, SaveSteps.GET_NEW_NAME2)
    dp.message.register(for_devs.get_voltage, SaveSteps.GET_VOLTAGE)
    dp.message.register(for_devs.get_cost, SaveSteps.GET_COST)
    dp.message.register(for_devs.get_link, SaveSteps.GET_LINK)
    dp.message.register(for_devs.get_category_1lvl, SaveSteps.GET_CATEGORY_1LVL)
    dp.message.register(for_devs.get_category_2lvl, SaveSteps.GET_CATEGORY_2LVL)
    dp.message.register(for_devs.get_activity, SaveSteps.GET_ACTIVITY)
    dp.message.register(for_devs.CancelActivity, SaveSteps.GET_NAME,
                        SaveSteps.GET_VOLTAGE, SaveSteps.GET_COST,
                        SaveSteps.GET_LINK, SaveSteps.GET_CATEGORY_1LVL,
                        SaveSteps.GET_CATEGORY_2LVL, SaveSteps.GET_SEARCH,
                        SaveSteps.GET_ACTIVITY_DELETE)

    dp.message.register(for_devs.delete_lamp, Command(commands='delete_lamp'))
    dp.message.register(for_devs.delete_res, SaveSteps.GET_DELETE)
    dp.message.register(for_devs.get_activity_delete, SaveSteps.GET_ACTIVITY_DELETE)
    dp.message.register(for_devs.get_confirmation, SaveSteps.GET_CONFIRM)

    dp.message.register(for_devs.get_update_lamp, Command(commands='update_lamp'))
    dp.message.register(for_devs.search_name, SaveSteps.SEARCH_NAME)
    dp.message.register(for_devs.get_new_name, SaveSteps.GET_NEW_NAME)
    dp.message.register(for_devs.get_activity_update, SaveSteps.GET_UPDATE)
    """Апдейт одного параметра"""
    dp.message.register(for_devs.get_edit, SaveSteps.GET_EDIT)
    dp.message.register(for_devs.edit_attr, SaveSteps.EDIT_ATTR)
    dp.message.register(for_devs.get_name_edit, SaveSteps.GET_NAME_EDIT)
    dp.message.register(for_devs.edit_name, SaveSteps.EDIT_NAME)
    dp.message.register(for_devs.get_voltage_edit, SaveSteps.GET_VOLTAGE_EDIT)
    dp.message.register(for_devs.edit_voltage, SaveSteps.EDIT_VOLTAGE)
    dp.message.register(for_devs.get_cost_edit, SaveSteps.GET_COST_EDIT)
    dp.message.register(for_devs.edit_cost, SaveSteps.EDIT_COST)
    dp.message.register(for_devs.get_link_edit, SaveSteps.GET_LINK_EDIT)
    dp.message.register(for_devs.edit_link, SaveSteps.EDIT_LINK)
    dp.message.register(for_devs.get_category_edit, SaveSteps.GET_PRED_EDIT)
    dp.message.register(for_devs.get_category_LITE1, SaveSteps.GET_CATEGORY_LITE1)
    dp.message.register(for_devs.get_category_LITE2, SaveSteps.GET_CATEGORY_LITE2)
    dp.message.register(for_devs.get_confirm_edits, SaveSteps.GET_CONFIRM_EDITS)

    dp.message.register(for_devs.show_id, Command(commands='id'))
    dp.message.register(for_devs.show_profile, Command(commands='profile'))
    dp.message.register(for_devs.answer_profile, SaveSteps.GET_ID)

    dp.message.register(users, Command(commands='all_users'))
    dp.message.register(dev_help, Command(commands='help_for_devs'))

    """Коллбеки"""
    dp.callback_query.register(answer_by_menu)

    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
