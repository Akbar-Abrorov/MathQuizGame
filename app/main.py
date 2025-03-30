from contextlib import asynccontextmanager
import uvicorn

from fastapi import FastAPI
from app.api_v1 import router as router_v1
from cfg.logger import logger
from models import Base,db_helper
from cfg import data_base

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield
app = FastAPI(title="MathQuizGame",lifespan=lifespan)

logger.info("APP STARTED")

app.include_router(router=router_v1, prefix=data_base.settings.api_v1_prefix)

@app.on_event("startup")
def startup_event():
    logger.info("Service 'Math Quiz Game' has started!")

@app.on_event("shutdown")
def shutdown_event():
    logger.info("Service 'Math Quiz Game' has stopped!")

    if __name__ == "__main__":
        uvicorn.run("main:app", reload=True)