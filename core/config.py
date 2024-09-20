from aiogram.utils.markdown import hide_link
from dotenv import load_dotenv
import os
load_dotenv()

TOKEN = os.getenv('TOKEN')
PASSWORD = os.getenv('PASSWORD')
link = hide_link('https://sun9-54.userapi.com/impg/L_3N0tftmZCouA88K5Nih5XeAZutoK5G38bfBg/C4b4xW12NnI.jpg?size=525x303&quality=96&sign=f0ba9a73b18f5b9ecc73efdbfa3ee859&type=album')
START = (f'\n<b><i>Почесть перед использованием</i></b>\n\n{link}'
         'Выберите категорию светильника, затем его тип. Вы увидите список с названиями, разделёнными через тире\n\n'
         '<b>Название светильника</b> - 1 часть(красный цвет)\nЕго <b>мощность</b> - 2 часть(синий цвет)\nПосле - указана <b>стоимость</b>')
HELP = """
/start    - Перезапуск бота

/menu     - Представляет каталог

/search   - Поиск светильника по названию

/website  - Ссылка на сайт

/for_devs - Блок для разработчиков
"""
HELP_FOR_DEVS = """
dev
"""
SEARCH_HELP = """
search
"""
