import sqlite3 as lite


class Database:
    def __init__(self, database, logger):
        self.database = database
        self.log = logger

    def __set(self, query):
        try:
            connect = lite.connect(self.database)
            cursor = connect.cursor()
            cursor.execute(query)
            connect.commit()
            connect.close()
        except lite.IntegrityError:
            self.log("Not unique")

    def __get(self, query):
        try:
            connect = lite.connect(self.database)
            cursor = connect.cursor()
            cursor.execute(query)

            result = [id[0] for id in cursor.fetchall()]

            connect.close()
            return result
        except lite.IntegrityError:
            self.log("Not unique")

    def set_ban(self, user_id):
        q = "INSERT INTO users_banned VALUES ({0})".format(user_id)
        self.__set(q)

    def get_all_banned(self):
        q = "SELECT id FROM users_banned"
        return self.__get(q)

    def unset_ban(self, user_id):
        q = "DELETE FROM users_banned WHERE id={0}".format(user_id)
        self.__set(q)

    def is_banned(self, user_id):
        q = "SELECT id FROM users_banned WHERE id={0}".format(user_id)
        return len(self.__get(q))

    def set_kicked(self, user_id, datetime):
        q = "INSERT INTO users_kicked VALUES ({0}, '{1}')".format(user_id, datetime)
        self.__set(q)

    def is_kicked(self, user_id):
        q = "SELECT * FROM users_kicked WHERE id={0}".format(user_id)
        return len(self.__get(q))

    def get_all_kicked(self):
        q = "SELECT id FROM users_kicked"
        return self.__get(q)

    def unset_kick(self, user_id):
        q = "DELETE FROM users_kicked WHERE id={0}".format(user_id)
        self.__set(q)

    def get_unkicked(self):
        q = "SELECT id FROM users_kicked WHERE unkick_time < datetime('now', 'localtime')"
        return self.__get(q)

    def get_admins(self):
        q = "SELECT id FROM users_admin"
        return self.__get(q)

    def get_creators(self):
        q = "SELECT id FROM users_admin WHERE permissions=1"
        return self.__get(q)

    def set_admin(self, user_id):
        q = "INSERT INTO users_admin VALUES ({0}, 0)".format(user_id)
        self.__set(q)

    def set_creator(self, user_id):
        q = "UPDATE users_admin SET permissions=1 WHERE id={0}".format(user_id)
        self.__set(q)

    def is_admin(self, user_id):
        q = "SELECT * FROM users_admin WHERE id={0}".format(user_id)
        return len(self.__get(q))

    def is_creator(self, user_id):
        q = "SELECT * FROM users_admin WHERE permissions=1 AND id={0}".format(user_id)
        return len(self.__get(q))

    def remove_admin(self, user_id):
        q = "DELETE FROM users_admin WHERE id={0}".format(user_id)
        self.__set(q)

    def set_warning(self, user_id):
        q = "INSERT INTO users_warnings VALUES ({0}, 1)".format(user_id)
        self.__set(q)

    def add_warning(self, user_id):
        q = "UPDATE users_warnings SET warnings = warnings + 1 WHERE id={0}".format(user_id)
        self.__set(q)

    def is_warning(self, user_id):
        q = "SELECT * from users_warnings WHERE id={0}".format(user_id)
        return len(self.__get(q))

    def count_warnings(self, user_id):
        q = "SELECT warnings FROM users_warnings WHERE id={0}".format(user_id)
        result = self.__get(q)
        return result[0] if result else 0

    def remove_warnings(self, user_id):
        q = "DELETE FROM users_warnings WHERE id={0}".format(user_id)
        self.__set(q)
