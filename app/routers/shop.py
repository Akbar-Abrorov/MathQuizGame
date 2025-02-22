from fastapi import APIRouter
from app.services.shop_logic import buy_item

router = APIRouter()

@router.post("/buy")
def buy(user_name: str, item_name: str):
    return buy_item(user_name, item_name)