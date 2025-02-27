import json
import logging
from cfg.logger import logger

USERS_FILE = "data/users.json"

def load_users():
    try:
        with open(USERS_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError as e:
        logger.error(f"Failed to load users.json: {str(e)}")
        users = [
            {"id": 1, "name": "Akbar", "points": 205, "items": {"Hint": 3, "Double Points": 0}, "questions": {"q1": "140 / 14", "q2": "10 - 5", "q3": "18 - 6"}, "answers": {"q3": {"answer": 12.0, "correct": true}}, "double_points_active": false},
            {"id": 2, "name": "Ulugbek", "points": 150, "items": {"Hint": 0, "Double Points": 1}, "questions": {}, "answers": {}, "double_points_active": false}
        ]
        save_users(users)
        return users

def save_users(users):
    try:
        with open(USERS_FILE, "w") as f:
            json.dump(users, f, indent=4)
    except Exception as e:
        logger.error(f"Failed to save users.json: {str(e)}")

def find_user(user_name, users=None):
    if users is None:
        users = load_users()
    return next((user for user in users if user["name"].lower() == user_name.lower()), None)

def create_user(user_name):
    users = load_users()
    if find_user(user_name, users):
        logger.warning(f"User action limited: User {user_name} already exists")
        return {"success": False, "message": "User already exists"}

    new_id = max((user["id"] for user in users), default=0) + 1
    new_user = {
        "id": new_id,
        "name": user_name,
        "points": 0,
        "items": {"Hint": 0, "Double Points": 0},
        "questions": {},
        "answers": {},
        "double_points_active": False
    }
    users.append(new_user)
    save_users(users)
    logger.info(f"User action: Created new user: {user_name} with ID {new_id}")
    return {"success": True, "message": f"User {user_name} created", "user": new_user}

def update_user_points(user_name, points_change):
    users = load_users()
    user = find_user(user_name, users)
    if not user:
        logger.error(f"User action failed: User {user_name} not found")
        return {"success": False, "message": "User not found"}

    user["points"] = max(0, user["points"] + points_change)
    save_users(users)
    logger.info(f"User action: Updated points for {user_name}: New balance {user['points']}")
    return {"success": True, "message": f"Points updated for {user_name}", "new_points": user["points"]}

def delete_user(user_name):
    users = load_users()
    user = find_user(user_name, users)
    if not user:
        logger.error(f"User action failed: User {user_name} not found")
        return {"success": False, "message": "User not found"}

    users = [u for u in users if u["name"].lower() != user_name.lower()]
    save_users(users)
    logger.info(f"User action: Deleted user: {user_name}")
    return {"success": True, "message": f"User {user_name} deleted"}

def get_user_stats(user_name):
    users = load_users()
    user = find_user(user_name, users)
    if not user:
        logger.error(f"User action failed: User {user_name} not found")
        return {"success": False, "message": "User not found"}

    stats = {
        "name": user["name"],
        "points": user["points"],
        "items": user["items"],
        "questions_answered": len(user["answers"]),
        "correct_answers": sum(1 for ans in user["answers"].values() if ans.get("correct", False)),
        "double_points_active": user["double_points_active"]
    }
    logger.info(f"User action: Retrieved stats for {user_name}")
    return {"success": True, "stats": stats}

def reset_user_progress(user_name):
    users = load_users()
    user = find_user(user_name, users)
    if not user:
        logger.error(f"User action failed: User {user_name} not found")
        return {"success": False, "message": "User not found"}

    user["points"] = 0
    user["items"] = {"Hint": 0, "Double Points": 0}
    user["questions"] = {}
    user["answers"] = {}
    user["double_points_active"] = False
    save_users(users)
    logger.info(f"User action: Reset progress for {user_name}")
    return {"success": True, "message": f"Progress reset for {user_name}"}

if __name__ == "__main__":
    print(create_user("Ali"))
    print(update_user_points("Ali", 50))
    print(get_user_stats("Ali"))
    print(reset_user_progress("Ali"))
    print(delete_user("Ali"))