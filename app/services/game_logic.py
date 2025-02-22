import random
from app.services.user_logic import get_user, update_user
from fastapi import HTTPException
from cfg.logger import logger

def generate_math_question(user_name: str):
    num1 = random.randint(1, 20)
    num2 = random.randint(1, 20)
    operation = random.choice(["+", "-", "*", "/"])

    if operation == "/":
        num1 = num2 * random.randint(1, 10)

    question = f"{num1} {operation} {num2}"
    correct_answer = eval(question)

    logger.info(f"Generated question: {question}, Answer: {correct_answer}")

    user = get_user(user_name)
    question_number = random.random()
    user["questions"].append({question_number : correct_answer})

    return {"question number": question_number, "question": question, "correct_answer": correct_answer}

def check_answer(user_name: str, user_answer: float):
    user = get_user(user_name)
    if not user:
        logger.warning(f"User {user_name} not found!")
        raise HTTPException(status_code=400, detail="User not found")

    question_data = generate_math_question.question
    correct_answer = question_data["correct_answer"]

    if abs(user_answer - correct_answer) < 0.001:
        user["points"] += 10
        message = f"Correct! {user_name} now has {user['points']} points."
        logger.info(message)
    else:
        user["points"] -= 5
        message = f"Wrong! {user_name} lost points. New balance: {user['points']}."
        logger.info(message)

    update_user(user)
    return {"success": True, "message": message, "question": question_data["question"]}