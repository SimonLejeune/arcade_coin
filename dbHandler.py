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
        self.c = self.conn.cursor()

    def manageUser(self, uid, email):
        self.c.execute('SELECT * FROM users')
        users = self.c.fetchall()
        for user in users:
            print "user : ", user
            if user is None:
                self.insertNew(uid, 1, email)
            else:
                self.removeCredit(uid)

    def insertNew(self, uid, credit=1, email=""):
        self.c.execute(
            'INSERT OR IGNORE INTO users(uid, credit, email, creation_date) VALUES( ?, ?, ?, datetime("now"))',
            (uid, credit, email))
        self.conn.commit()
        return 'created'

    def removeCredit(self, uid):
        self.c.execute('SELECT * FROM users WHERE uid=' + uid)
        user = self.c.fetchone()
        if user is None:
            return 'reject'
        credits = user[3]
        if user is None or credits < 1:
            return 'reject'
        self.c.execute('UPDATE users SET credit=' + str(credits - 1) + ' WHERE uid=' + str(uid))
        self.conn.commit()
        return "accept"

    def addAllCredit(self, credit=1):
        self.c.execute('update users SET credit={} where credit<{}'.format(credit, credit))
        self.conn.commit()
