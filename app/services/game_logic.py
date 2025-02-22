import json
import random

def save_users(users):
    with open("users.json", "w") as f:
        json.dump(users, f)

def load_users():
    try:
        with open("users.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        users = [
            {"id": 1, "name": "Akbar", "points": 225, "items": {"Hint": 1, "Double Points": 0}, "questions": {}, "answers": {}, "double_points_active": False},
            {"id": 2, "name": "Ulugbek", "points": 150, "items": {"Hint": 0, "Double Points": 1}, "questions": {}, "answers": {}, "double_points_active": False}
        ]
        save_users(users)
        return users

def find_user(user_name, users):
    for user in users:
        if user["name"] == user_name:
            return user
    return None

users = load_users()

def generate_math_question(user_name):
    user = find_user(user_name, users)
    if user == None:
        print("User not found")
        return False

    num1 = random.randint(1, 20)
    num2 = random.randint(1, 20)
    operation = random.choice(["+", "-", "*", "/"])

    if operation == "/":
        num1 = num2 * random.randint(1, 10)

    question = f"{num1} {operation} {num2}"
    correct_answer = eval(question)

    if "questions" not in user:
        user["questions"] = {}
    if "answers" not in user:
        user["answers"] = {}

    question_count = len(user["questions"]) + 1
    question_id = f"q{question_count}"
    user["questions"][question_id] = question
    save_users(users)

    print(f"Generated question for {user_name}: {question}")
    return {"question_id": question_id, "question": question}

def check_answer(user_name, question_id, user_answer):
    user = find_user(user_name, users)
    if user == None:
        print(f"User {user_name} not found!")
        return False

    if "questions" not in user or question_id not in user["questions"]:
        print("Question not found for this user")
        return False

    question_text = user["questions"][question_id]
    try:
        correct_answer = eval(question_text)
    except (ZeroDivisionError, SyntaxError, NameError):
        print(f"Error: Cannot calculate answer for question '{question_text}'")
        return False

    points_to_add = 10
    if user.get("double_points_active", False):
        points_to_add = points_to_add * 2
        user["double_points_active"] = False
        save_users(users)

    if abs(user_answer - correct_answer) < 0.001:
        user["points"] = user["points"] + points_to_add
        print(f"Correct! {user_name} now has {user['points']} points.")
    else:
        user["points"] = user["points"] - 5
        print(f"Wrong! {user_name} lost points. New balance: {user['points']}.")

    answer_id = f"ans{question_id[1:]}"
    user["answers"][answer_id] = user_answer
    save_users(users)

    return {
        "message": "Answer checked",
        "question": question_text,
        "correct_answer": correct_answer,
        "user_answer": user_answer
    }

if __name__ == "__main__":
    question_response = generate_math_question("Akbar")
    if question_response:
        answer_response = check_answer("Akbar", question_response["question_id"], 42.0)
        print(answer_response)

    question_response_ulugbek = generate_math_question("Ulugbek")
    if question_response_ulugbek:
        answer_response_ulugbek = check_answer("Ulugbek", question_response_ulugbek["question_id"], 15.0)
        print(answer_response_ulugbek)