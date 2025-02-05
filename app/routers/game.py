from fastapi import APIRouter
from app.services.game_logic import generate_math_question, check_answer

router = APIRouter()

@router.get("/question")
def get_question():
    return generate_math_question()

@router.post("/answer")
def submit_answer(user_name: str, user_answer: int):
    return check_answer(user_name, user_answer)