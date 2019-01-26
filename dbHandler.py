import sqlite3

class Connection:
    def __init__(self, dbName):
        self.conn = sqlite3.connect(dbName)
        self.conn.row_factory = sqlite3.Row
        self.c = self.conn.cursor()
        self.insertNext = False

    def checkUser(self):
        print "check user"

    def insertNew(self):
        print "insert new"

    def removeCredits(self):
        print "remove credits"

    def addAllCredits(self):
        print "addAll Credits"