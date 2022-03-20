from tinydb import TinyDB
import time

db = TinyDB('database.json')

if not db.get(doc_id=1):
    db.insert({"prevTime": time.time(),
              "twitter": [], "instagram": []})

db.update({"twitter": [
          "something"], "instagram": ["something"]}, doc_ids=[1])
