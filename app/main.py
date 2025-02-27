from fastapi import FastAPI
from app.routers import game, shop
from cfg.logger import logger

app = FastAPI(title="MathQuizGame")

logger.info("APP STARTED")

app.include_router(game.router, prefix="/quiz", tags=["Quiz"])
app.include_router(shop.router, prefix="/shop", tags=["Shop"])

@app.on_event("startup")
def startup_event():
    logger.info("Service 'Math Quiz Game' has started!")

@app.on_event("shutdown")
def shutdown_event():
    logger.info("Service 'Math Quiz Game' has stopped!")