import datetime
import json
import os

USERS_FILE = "data/users.json"


def load_users():
    if not os.path.exists(USERS_FILE):
        return []
    with open(USERS_FILE, "r") as f:
        return json.load(f)


def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=4)

def is_premium(username):

    import json
    from datetime import datetime

    with open("data/users.json", "r") as f:
        users = json.load(f)

    user = users.get(username)

    if not user:
        return False

    start_date = datetime.fromisoformat(user["start_date"])
    now = datetime.now()

    if (now - start_date).days <= 30:
        return True

    return user.get("premium", False) 


def register(username, password):
    
    try:
        with open("data/users.json", "r") as f:
            users = json.load(f)
    except:
        users = {}

    if username in users:
        return False

    users[username] = {
        "password": password,
        "premium": True,
        "start_date": str(datetime.datetime.now())
    }

    with open("data/users.json", "w") as f:
        json.dump(users, f, indent=4)

    return True


def login(username, password):

    import json

    with open("data/users.json", "r") as f:
        users = json.load(f)

    if username in users:
        if users[username]["password"] == password:
            return True

    return False