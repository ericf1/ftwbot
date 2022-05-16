# updates all timestamps and tests the json file's structure
import time
from bot import updateDoc, db, doc


def main():
    i = 0
    for serverID in db.tables():
        print(doc(serverID).get("prevTime"))
        if(doc(serverID).get("prevTime") == None):
            updateDoc(serverID, {"prevTime": int(time.time())})
            continue
        updateDoc(serverID, {"prevTime": int(time.time())})
        i = i + 1
    return i


if __name__ == "__main__":
    print(main())
