from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault


commands = [
        BotCommand(command='start', description='Запуск бота'),
        BotCommand(command='menu', description='Позволяет выбрать категорию светильников'),
        BotCommand(command='search', description='Поиск светильника по названию'),
        BotCommand(command='search_help', description='Подробнее о поиске'),
        BotCommand(command='website', description='Ссылка на сайт'),
        BotCommand(command='help', description='Помощь'),
        BotCommand(command='for_devs', description='Для владельцев и разработчиков')
    ]

commands_for_devs = [
        BotCommand(command='add_lamp', description='Добавление светильника в базу данных'),
        BotCommand(command='delete_lamp', description='Удаление светильника из базы данных'),
        BotCommand(command='update_lamp', description='Обновление данных о светильнике'),
        BotCommand(command='id', description='Позволяет узнать id аккаунта'),
        BotCommand(command='all_users', description='Показывает всех пользователей в базе данных'),
        BotCommand(command='profile', description='Высылает профиль пользователя по id'),
        BotCommand(command='help_for_devs', description='Помощь для разработчиков')
]


async def set_commands(bot: Bot):
    await bot.set_my_commands(commands, BotCommandScopeDefault())


async def set_dev_commands(bot: Bot):
    commands.extend(commands_for_devs)
    await bot.set_my_commands(commands, BotCommandScopeDefault())
