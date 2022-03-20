from tinydb import TinyDB, Query

db = TinyDB('database.json')

db.insert({'time': 124125552})
