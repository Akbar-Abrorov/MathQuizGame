import json
from app.services.user_logic import get_user, update_user,load_users


def load_items():
    with open("data/items.json", "r") as file:
        return json.load(file)


def buy_item(user_name: str, item_name: str):
    users = load_users()
    user = get_user(user_name)
    if not user:
        return {"success": False, "message": "User not found"}

    items = load_items()
    item = next((i for i in items if i["name"].lower() == item_name.lower()), None)

    if not item:
        return {"success": False, "message": "Item not found"}
    if user["points"] < item["price"]:
        return {"success": False, "message": "Not enough points"}

    user["points"] -= item["price"]
    user["items"][item_name] = user["items"].get(item_name, 0) + 1
    update_user(user)

    return {"success": True, "message": f"You bought {item_name}", "new_points": user["points"]}