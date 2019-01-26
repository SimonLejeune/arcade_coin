import sqlite3
from sqlite3 import Error


class Connection:
    def __init__(self, dbName, create_db):
        print "init"
        conn = self.create_connection(dbName)
        self.c = conn.cursor()
        if conn is not None:
            # create projects table
            self.create_table(conn, create_db)
        else:
            print("Error! cannot create the database connection.")

    def checkUser(self, ID, email):
        print "check user"
        self.c.execute('SELECT * FROM user')
        users = self.c.fetchall()
        for user in users:
            print "here a user : ", user
            if user == None:
                self.insertNew(ID, 1, 1, email)
            else:
                self.removeCredits(ID)

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

    def addAllCredits(self, credit=1):
        print "addAll Credits"
        self.c.execute('update user SET credit={} where credit<{}'.format(credit, credit))
        self.conn.commit()

    def create_connection(self, dbName):
        """ create a database connection to the SQLite database
            specified by db_file
        :param db_file: database file
        :return: Connection object or None
        """
        try:
            conn = sqlite3.connect(dbName)
            return conn
        except Error as e:
            print(e)

        return None

    def create_table(self, conn, create_table_sql):
        """ create a table from the create_table_sql statement
        :param conn: Connection object
        :param create_table_sql: a CREATE TABLE statement
        :return:
        """
        try:
            c = conn.cursor()
            c.execute(create_table_sql)
        except Error as e:
            print(e)
