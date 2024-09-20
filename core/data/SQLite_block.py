import sqlite3
from core.data.redis_storage import redis
import pickle


class SQLiter:
    def __init__(self, database):
        """Соединение и Подключение"""
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()

    def get_lamp(self, lamp_name):
        """Поиск по названию светильника"""
        with self.connection:
            return self.cursor.execute("SELECT * FROM `lamps` WHERE `name` LIKE ? ORDER BY `cost` ASC",
                                       ('%'+lamp_name+'%',)).fetchall()

    def lamp_exists(self, lamp_name):
        """Проверка на наличие светильника в БД"""
        with self.connection:
            res = self.cursor.execute("SELECT `id` FROM `lamps` WHERE `name` = ?", (lamp_name,)).fetchall()
            return bool(len(res))

    def add_lamp(self, lamp_name, voltage, cost, link, category):
        """Добавление светильника"""
        with self.connection:
            return self.cursor.execute("INSERT INTO `lamps` (`name`, `voltage`, `cost`, `link`, `category`) VALUES(?,?,?,?,?)",
                                       (lamp_name, voltage, cost, link, category))

    async def search_lamp(self, search_name, current, cache_name=None) -> 'tuple[list, int]':
        """Поиск светильников для `меню` по запросу"""
        res = await redis.get('res')
        name = await redis.get(cache_name)
        if res and name:
            res = pickle.loads(res)
        else:
            res = db.get_lamp(search_name)
            await redis.set(name=cache_name, value=cache_name, ex=60)
            await redis.set(name='res', value=pickle.dumps(res), ex=60)
        last = len(res)
        current = (current - 1) * 10
        current_last = current + 10
        res = (res[current:current_last]), last
        return res

    def lamp_delete(self, lamp_name):
        """Удаление светильника"""
        with self.connection:
            return self.cursor.execute("DELETE FROM `lamps` WHERE `name` = ?", (lamp_name,))

    def update_lamp(self, lamp_name, voltage, cost, link, category, old_name):
        """Обновление данных светильника"""
        return self.cursor.execute("UPDATE `lamps` SET `name` = ?, `voltage` = ?, `cost` = ?, `link` = ?, `category` = ? WHERE `name` = ?",
                                   (lamp_name, voltage, cost, link, category, old_name))

    def update_attr(self, column, attr, name):
        """Обновление одного параметра"""
        return self.cursor.execute(f"UPDATE `lamps` SET `{column}` = ? WHERE `name` = ?", (attr, name))

    def name_cost_by_category(self, category, num):
        """8 светильников (название и стоимость) по категории"""
        with self.connection:
            return self.cursor.execute("SELECT * FROM (SELECT `name`, `cost` FROM `lamps` WHERE `category` = ? ORDER BY `cost` ASC) LIMIT 8 OFFSET ?",
                                       (category, num)).fetchall()

    def get_len_subcategory(self, subcategory):
        """кол-во светильников одной категории"""
        with self.connection:
            return len(self.cursor.execute("SELECT `id` FROM `lamps` WHERE `category` = ?", (subcategory,)).fetchall())

    def category_exists(self, category):
        """Проверка колл-даты на категорию
        см. callback_main.py"""
        with self.connection:
            res = self.cursor.execute("SELECT `id` FROM `lamps` WHERE `category` = ? LIMIT 1", (category,)).fetchall()
            return bool(len(res))

    def user_exists(self, tg_id):
        """Проверка на наличие id в БД"""
        with self.connection:
            return self.cursor.execute("SELECT * FROM `users` WHERE `tg_id` = ?", (tg_id,)).fetchall()

    def add_user(self, tg_id, status=False):
        """Добавление пользователя"""
        with self.connection:
            return self.cursor.execute("INSERT INTO `users` (`tg_id`, `status`) VALUES(?,?)", (tg_id, status))

    def add_dev(self, tg_id):
        """Изменения статуса пользователя на разработчика"""
        with self.connection:
            return self.cursor.execute("UPDATE `users` SET `status` = 1 WHERE `tg_id` = ?", (tg_id,))

    def all_users(self):
        """Показывает всех пользователей в БД"""
        with self.connection:
            return self.cursor.execute("SELECT `tg_id`, `status` FROM `users`").fetchall()

    def close(self):
        """Закрытие соединения"""
        self.connection.close()


db = SQLiter(r'core\DeLED_data.db')
