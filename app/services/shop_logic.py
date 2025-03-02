import json
import logging
from typing import Dict, Any, Optional
from cfg.logger import logger

SHOP_ITEMS_FILE = "data/items.json"
USERS_FILE = "data/users.json"

SHOP_ITEMS = {
    "Hint": {"price": 30, "effect": "Gives a hint for the next question"},
    "Double Points": {"price": 50, "effect": "Doubles points for the next correct answer"}
}

class ShopSystem:
    def __init__(self):
        self.shop_items = self.load_shop_items()
        self.users = self.load_users()

    def load_shop_items(self) -> dict:
        try:
            with open(SHOP_ITEMS_FILE, "r") as f:
                return json.load(f)
        except FileNotFoundError as e:
            logger.error(f"Failed to load shop_items.json: {str(e)}")
            self.save_shop_items()
            return SHOP_ITEMS
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in shop_items.json: {str(e)}")
            raise

    def save_shop_items(self) -> None:
        try:
            with open(SHOP_ITEMS_FILE, "w") as f:
                json.dump(self.shop_items, f, indent=4)
        except Exception as e:
            logger.error(f"Failed to save shop_items.json: {str(e)}")
            raise

    def load_users(self) -> list:
        try:
            with open(USERS_FILE, "r") as f:
                users = json.load(f)
                return users
        except FileNotFoundError as e:
            logger.error(f"Failed to load users.json: {str(e)}")
            users = [
                {"id": 1, "name": "Akbar", "points": 205, "items": {"Hint": 3, "Double Points": 0},
                 "questions": {"q1": "140 / 14", "q2": "10 - 5", "q3": "18 - 6"},
                 "answers": {"q3": {"answer": 12.0, "correct": True}}, "double_points_active": False},
                {"id": 2, "name": "Ulugbek", "points": 150, "items": {"Hint": 0, "Double Points": 1},
                 "questions": {}, "answers": {}, "double_points_active": False}
            ]
            self.save_users(users)
            return users
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in users.json: {str(e)}")
            raise

    def save_users(self, users: list) -> None:
        try:
            with open(USERS_FILE, "w") as f:
                json.dump(users, f, indent=4)
        except Exception as e:
            logger.error(f"Failed to save users.json: {str(e)}")
            raise

    def find_user(self, user_name: str) -> Optional[Dict[str, Any]]:
        return next((user for user in self.users if user["name"].lower() == user_name.lower()), None)

    def buy_item(self, user_name: str, item_name: str) -> Dict[str, Any]:
        user = self.find_user(user_name)
        if not user:
            logger.error(f"User action failed: User {user_name} not found")
            return {"success": False, "message": "User not found"}

        item = self.shop_items.get(item_name)
        if not item:
            logger.error(f"User action failed: Item {item_name} not found in shop")
            return {"success": False, "message": "Item not found"}

        if user["points"] < item["price"]:
            logger.warning(f"User action limited: {user_name} has insufficient points to buy {item_name}")
            return {"success": False, "message": "Not enough points to buy this item"}

        user["points"] -= item["price"]
        user["items"][item_name] = user["items"].get(item_name, 0) + 1
        self.save_users(self.users)
        logger.info(f"User action: {user_name} bought {item_name} for {item['price']} points")
        return {
            "success": True,
            "message": f"{user_name} bought {item_name}!",
            "item": item_name,
            "price": item["price"],
            "new_balance": user["points"]
        }

    def check_item_status(self, user_name: str, item_name: str) -> Dict[str, Any]:
        user = self.find_user(user_name)
        if not user:
            logger.error(f"User action failed: User {user_name} not found")
            return {"success": False, "message": "User not found"}

        item = self.shop_items.get(item_name)
        if not item:
            logger.error(f"User action failed: Item {item_name} not found in shop")
            return {"success": False, "message": "Item not found"}

        item_count = user["items"].get(item_name, 0)
        logger.info(f"User action: Checked item status for {user_name}: {item_count} {item_name}(s) owned")
        return {
            "success": True,
            "message": f"{user_name} owns {item_count} {item_name}(s).",
            "item": item_name,
            "price": item["price"],
            "effect": item["effect"],
            "quantity": item_count
        }

    def use_item(self, user_name: str, item_name: str) -> Dict[str, Any]:
        user = self.find_user(user_name)
        if not user:
            logger.error(f"User action failed: User {user_name} not found")
            return {"success": False, "message": "User not found"}

        if user["items"].get(item_name, 0) == 0:
            logger.warning(f"User action limited: No {item_name} available for {user_name} to use")
            return {"success": False, "message": f"No {item_name} available to use"}

        if item_name == "Hint":
            hint_message = "Hint for next question: Focus on basic arithmetic operations (+, -, *, /, **, %, //)!"
            user["items"][item_name] -= 1
            self.save_users(self.users)
            logger.info(f"User action: {user_name} used a {item_name}: {hint_message}")
            return {"success": True, "message": hint_message}
        elif item_name == "Double Points":
            user["items"][item_name] -= 1
            user["double_points_active"] = True
            self.save_users(self.users)
            logger.info(f"User action: {user_name} activated Double Points for the next correct answer")
            return {"success": True, "message": "Double Points activated for the next correct answer"}

        logger.error(f"User action failed: Item {item_name} cannot be used at this time for {user_name}")
        return {"success": False, "message": "Item cannot be used at this time"}

if __name__ == "__main__":
    shop = ShopSystem()
    print(shop.buy_item("Akbar", "Hint"))
    print(shop.check_item_status("Akbar", "Hint"))
    print(shop.use_item("Akbar", "Hint"))