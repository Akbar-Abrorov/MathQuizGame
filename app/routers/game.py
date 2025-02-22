from fastapi import APIRouter
from app.services.game_logic import generate_math_question, check_answer

router = APIRouter()

@router.post("/question")
def get_question(user_name: str):
    return generate_math_question(user_name)

@router.post("/answer")
def submit_answer(user_name: str, user_answer: float):
    return check_answer(user_name, user_answer)