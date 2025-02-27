from fastapi import APIRouter
from app.services.shop_logic import ShopSystem
from cfg.logger import logger

router = APIRouter()
shop = ShopSystem()

@router.post("/buy")
def buy(user_name: str, item_name: str):
    logger.info(f"User action: {user_name} attempted to buy {item_name}")
    return shop.buy_item(user_name, item_name)

@router.get("/status/{user_name}/{item_name}")
def item_status(user_name: str, item_name: str):
    logger.info(f"User action: {user_name} checked status of {item_name}")
    return shop.check_item_status(user_name, item_name)

@router.post("/use")
def use(user_name: str, item_name: str):
    logger.info(f"User action: {user_name} attempted to use {item_name}")
    return shop.use_item(user_name, item_name)