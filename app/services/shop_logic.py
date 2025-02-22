import json

shop_items = {
    "Hint": {"price": 30, "effect": "Gives a hint for the next question"},
    "Double Points": {"price": 50, "effect": "Doubles points for the next correct answer"}
}

def save_shop_items():
    with open("shop_items.json", "w") as f:
        json.dump(shop_items, f)

def load_shop_items():
    try:
        with open("shop_items.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        save_shop_items()
        return shop_items

def save_users(users):
    with open("users.json", "w") as f:
        json.dump(users, f)

def load_users():
    try:
        with open("users.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        users = [
            {"id": 1, "name": "Akbar", "points": 225, "items": {"Hint": 1, "Double Points": 0}, "double_points_active": False},
            {"id": 2, "name": "Ulugbek", "points": 150, "items": {"Hint": 0, "Double Points": 1}, "double_points_active": False}
        ]
        save_users(users)
        return users

def find_user(user_name, users):
    for user in users:
        if user["name"] == user_name:
            return user
    return None

shop_items = load_shop_items()
users = load_users()

def buy_item(user_name, item_name):
    user = find_user(user_name, users)
    if user == None:
        return {"success": False, "message": "User not found"}

    item = shop_items.get(item_name)
    if item == None:
        return {"success": False, "message": "Item not found"}

    if user["points"] < item["price"]:
        return {"success": False, "message": "Not enough points to buy this item"}

    user["points"] = user["points"] - item["price"]
    if "items" not in user:
        user["items"] = {}
    if item_name in user["items"]:
        user["items"][item_name] = user["items"][item_name] + 1
    else:
        user["items"][item_name] = 1
    save_users(users)

    response = {
        "success": True,
        "message": f"{user_name} bought {item_name}!",
        "item": item_name,
        "price": item["price"],
        "new_balance": user["points"]
    }
    print(response["message"])
    return response

def view_shop_items():
    print("Available items in the shop:")
    for item_name, details in shop_items.items():
        print(f"{item_name} - Price: {details['price']}, Effect: {details['effect']}")
    return True

def check_item_status(user_name, item_name):
    user = find_user(user_name, users)
    if user == None:
        print("User not found")
        return False

    item = shop_items.get(item_name)
    if item == None:
        print("Item not found")
        return False

    item_count = user["items"].get(item_name, 0)
    print(f"{user_name} owns {item_count} {item_name}(s).")
    print(f"Item: {item_name}, Price: {item['price']}, Effect: {item['effect']}")
    return True

def use_item(user_name, item_name):
    user = find_user(user_name, users)
    if user == None:
        print("User not found")
        return False

    if "items" not in user or user["items"].get(item_name, 0) == 0:
        print(f"No {item_name} available to use")
        return False

    if item_name == "Hint":
        hint_message = "Hint for next question: Focus on basic arithmetic operations (+, -, *, /)!"
        user["items"][item_name] = user["items"][item_name] - 1
        save_users(users)
        print(f"{user_name} used a {item_name}. {hint_message}")
        return {"message": hint_message}
    elif item_name == "Double Points":
        user["items"][item_name] = user["items"][item_name] - 1
        user["double_points_active"] = True
        save_users(users)
        print(f"{user_name} activated Double Points for the next correct answer!")
        return True

    print("Item cannot be used at this time")
    return False

if __name__ == "__main__":
    buy_response = buy_item("Ulugbek", "Hint")
    print(buy_response)
    view_shop_items()
    check_item_status("Akbar", "Hint")
    use_item("Ulugbek", "Hint")