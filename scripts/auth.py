import json

FILE = "data/users.json"

def load_users():
    try:
        with open(FILE) as f:
            return json.load(f)
    except:
        return {}

def save_users(users):
    with open(FILE, "w") as f:
        json.dump(users, f, indent=4)

def is_premium(username):
    users = load_users()
    return users.get(username, {}).get("premium", False)

def activate_premium(username):
    users = load_users()
    if username not in users:
        users[username] = {}
    users[username]["premium"] = True
    save_users(users)