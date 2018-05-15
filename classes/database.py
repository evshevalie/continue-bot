import sqlite3 as lite

class Database:
    def __init__(self, database):
        self.connect = lite.connect("../database/continue_bot.db")
        self.cursor = self.connect.cursor()
