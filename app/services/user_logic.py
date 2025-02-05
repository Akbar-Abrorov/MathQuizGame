import json

def load_users():
    try:
        with open("data/users.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def save_users(users):
    with open("data/users.json", "w") as file:
        json.dump(users, file, indent=4)

def get_user(user_name):
    users = load_users()
    return next((u for u in users if u["name"] == user_name), None)

def update_user(user):
    users = load_users()
    for i, u in enumerate(users):
        if u["name"] == user["name"]:
            users[i] = user
            break
    save_users(users)