from fastapi import APIRouter
from app.services.game_logic import MathQuizGame
from cfg.logger import logger


router = APIRouter()
game = MathQuizGame()

@router.post("/question")
def get_question(user_name: str):
    logger.info(f"User action: {user_name} requested a new question")
    return game.generate_math_question(user_name)

@router.post("/answer")
def submit_answer(user_name: str, question_id: str, user_answer: float):
    logger.info(f"User action: {user_name} submitted answer for question {question_id}")
    return game.check_answer(user_name, question_id, user_answer)

@router.get("/stats/{user_name}")
def get_stats(user_name: str):
    logger.info(f"User action: {user_name} requested stats")
    return game.get_user_stats(user_name)

@router.post("/reset/{user_name}")
def reset_progress(user_name: str):
    logger.info(f"User action: {user_name} requested progress reset")
    return game.reset_user_progress(user_name)