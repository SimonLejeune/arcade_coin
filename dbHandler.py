import sqlite3
from sqlite3 import Error


class Connection:
    def __init__(self, dbName):
        self.conn = sqlite3.connect(dbName)
        if self.conn is not None:
            # create projects table
            try:
                c = self.conn.cursor()
                c.execute(
                    'CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY AUTOINCREMENT, uid TEXT UNIQUE, credit INTEGER, email TEXT, creation_date DATETIME, last_played DATETIME);')
            except Error as e:
                print(e)
        self.conn.row_factory = sqlite3.Row
        self.c = self.conn.cursor()
        self.insertNext = True

    def insertNew(self, uid, credit=1, email=""):
        self.c.execute(
            'INSERT OR IGNORE INTO users(uid, credit, email, creation_date) VALUES( {}, {}, {}, "{}", datetime("now"))'.format(
                uid, credit, email))
        self.conn.commit()
        self.insertNext = False
        return 'created'

    def insertTimeOut(self):
        self.insertNext = False

    def removeCredit(self, uid, email):
        if self.insertNext:
            return self.insertNew(uid, email)
        self.c.execute('SELECT * FROM users WHERE uid=' + str(uid))
        user = self.c.fetchone()
        if user == None:
            return 'reject'
        type = user[2]
        credits = user[3]
        if user is None or credits < 1 and type > 0:
            return 'reject'

        self.c.execute('UPDATE users SET credit=' + str(credits - 1) + ' WHERE uid=' + str(uid))
        self.conn.commit()
        return "accept"

    def addAllCredit(self, credit=10):
        self.c.execute('update users SET credit={} where credit<{}'.format(credit, credit))
        self.conn.commit()
