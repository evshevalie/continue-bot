import sqlite3 as lite

class Database:
    def __init__(self, database):
        self.connect = lite.connect(database)
        self.cursor = self.connect.cursor()

    def set_ban(self, user_id):
        q = "INSERT INTO users_banned VALUES ('{0}')".format(user_id)
        self.cursor.execute(q)
        self.connect.commit()

    def get_all_banned(self):
        q = "SELECT id FROM users_banned"
        self.cursor.execute(q)
        return self.cursor.fetchall()

    def unset_ban(self, user_id):
        q = "DELETE FROM users_banned WHERE id='{0}'".format(user_id)
        self.cursor.execute(q)
        self.connect.commit()

    def set_kicked(self, user_id, datetime):
        q = "INSERT INTO users_kicked VALUES ('{0}', '{1}')".format(user_id, datetime)
        self.cursor.execute(q)
        self.connect.commit()

    def get_all_kicked(self):
        q = "SELECT * FROM users_kicked"
        self.cursor.execute(q)
        return self.cursor.fetchall()

    def unset_kick(self, user_id):
        q = "DELETE FROM users_kicked WHERE id='{0}'".format(user_id)"
        self.cursor.execute(q)
        self.connect.commit()
