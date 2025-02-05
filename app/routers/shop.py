from fastapi import APIRouter
from app.services.shop_logic import load_items, buy_item

router = APIRouter()

@router.get("/items")
def get_items():
    return load_items()
@router.get("/buy")
def buy(user_name: str, item_name: str):
    return buy_item(user_name, item_name)