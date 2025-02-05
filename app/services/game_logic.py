import random
from app.services.user_logic import get_user, update_user
from fastapi import HTTPException
from cfg.logger import logger  # Import logger

def generate_math_question():
    num1 = random.randint(1, 20)
    num2 = random.randint(1, 20)
    operation = random.choice(["+", "-"])
    question = f"{num1} {operation} {num2}"
    answer = eval(question)

    logger.info(f"Generated question: {question}, Answer: {answer}")  # Log question generation

    return {"question": question, "answer": answer}

def check_answer(user_name: str, user_answer: int):
    user = get_user(user_name)
    if not user:
        logger.warning(f"User {user_name} not found!")  # Log warning
        raise HTTPException(status_code=400, detail="User not found")

    question_data = generate_math_question()
    correct_answer = question_data["answer"]

    if user_answer == correct_answer:
        user["points"] += 10
        message = f"Correct! {user_name} now has {user['points']} points."
        logger.info(message)  # Log success
    else:
        user["points"] -= 5
        message = f"Wrong! {user_name} lost points. New balance: {user['points']}."
        logger.info(message)  # Log failure

    update_user(user)
    return {"success": True, "message": message, "question": question_data["question"]}