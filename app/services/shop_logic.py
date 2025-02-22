import json
from app.services.user_logic import get_user, update_user
from fastapi import HTTPException
from cfg.logger import logger

shop_items = {
    "Hint": {"price": 30, "effect": "Gives a hint for the next question"},
    "Double Points": {"price": 50, "effect": "Doubles points for the next correct answer"}
}

def buy_item(user_name: str, item_name: str):
    user = get_user(user_name)
    if not user:
        raise HTTPException(status_code=400, detail="User not found")

    item = shop_items.get(item_name)
    if not item:
        raise HTTPException(status_code=400, detail="Item not found")

    if user["points"] < item["price"]:
        raise HTTPException(status_code=400, detail="Not enough points to buy this item")

    user["points"] -= item["price"]
    user["items"].append(item_name)
    update_user(user)

    message = f"{user_name} bought {item_name}! New balance: {user['points']} points."
    logger.info(message)

    return {"success": True, "message": message, "new_balance": user["points"]}