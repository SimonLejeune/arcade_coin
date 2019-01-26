settings = {'database': 'testData.db', # this is your database location
'startupCredits': '1', # add credits on restart, this number sets the credits to the alloted amount ON RESTART if they are under that$
'create_users_table': 'CREATE TABLE IF NOT EXISTS user(id INTEGER PRIMARY KEY AUTOINCREMENT, tag TEXT UNIQUE, type INTEGER, credit INTEGER, name TEXT, creation_date DATETIME, last_played DATETIME);'
}

