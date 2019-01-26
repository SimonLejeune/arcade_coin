import sqlite3

class Connection:
    def __init__(self, dbName):
        self.conn = sqlite3.connect(dbName)
        self.conn.row_factory = sqlite3.Row
        self.c = self.conn.cursor()
        self.insertNext = False

    def checkUser(self, ID, email):
        print "check user"
        self.c.execute('SELECT * FROM user')
        rows = self.c.fetchall()
        for row in rows:
            print(row)
        #if user == None:
            #self.insertNew(ID, 1, 10, email)
        #else:
            #self.removeCredits(ID)


    def insertNew(self, ID, type=1, credit=1, name='user'):
        print "insert new"
        self.c.execute(
            'INSERT OR IGNORE INTO user(tag, type, credit, name, creation_date) VALUES( {}, {}, {}, "{}", datetime("now"))'.format(
                ID, type, credit, name))
        self.conn.commit()
        self.insertNext = False

    def removeCredits(self, ID):
        print "remove credits"
        self.c.execute('SELECT * FROM user WHERE tag=' + str(ID))
        user = self.c.fetchone()
        if user == None:
            return 'reject'
        type = user[2]
        credits = user[3]
        if credits < 1 and type > 0:
            return 'reject'
        self.c.execute('UPDATE user SET credit=' + str(credits - 1) + ' WHERE tag=' + str(ID))
        self.conn.commit()
        return 'accept'

    def addAllCredits(self, credit = 1):
        print "addAll Credits"
        self.c.execute('update user SET credit={} where credit<{}'.format(credit, credit))
        self.conn.commit()