import json
import random
import logging
from typing import Dict, Any, Optional
from cfg.logger import logger

USERS_FILE = "data/users.json"


class MathQuizGame:
    def __init__(self):
        self.users = self.load_users()

    def load_users(self) -> list:
        try:
            with open(USERS_FILE, "r") as f:
                users = json.load(f)
                for user in users:
                    self._ensure_user_structure(user)
                return users
        except FileNotFoundError as e:
            logger.error(f"Failed to load users.json: {str(e)}")
            users = [
                {"id": 1, "name": "Akbar", "points": 205, "items": {"Hint": 3, "Double Points": 0},
                 "questions": {"q1": "140 / 14", "q2": "10 - 5", "q3": "18 - 6"},
                 "answers": {"q3": {"answer": 12.0, "correct": True}}, "double_points_active": False},
                {"id": 2, "name": "Ulugbek", "points": 150, "items": {"Hint": 0, "Double Points": 1},
                 "questions": {}, "answers": {}, "double_points_active": False}
            ]
            self.save_users(users)
            return users
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in users.json: {str(e)}")
            raise

    def save_users(self, users: list) -> None:
        try:
            with open(USERS_FILE, "w") as f:
                json.dump(users, f, indent=4)
        except Exception as e:
            logger.error(f"Failed to save users.json: {str(e)}")
            raise

    def _ensure_user_structure(self, user: Dict[str, Any]) -> None:
        required_fields = {"points": 0, "items": {"Hint": 0, "Double Points": 0},
                           "questions": {}, "answers": {}, "double_points_active": False}
        for field, default in required_fields.items():
            if field not in user:
                user[field] = default
            elif field in ["items", "questions", "answers"]:
                if not isinstance(user[field], dict):
                    user[field] = default

    def find_user(self, user_name: str) -> Optional[Dict[str, Any]]:
        return next((user for user in self.users if user["name"].lower() == user_name.lower()), None)

    def generate_math_question(self, user_name: str) -> Dict[str, Any]:
        user = self.find_user(user_name)
        if not user:
            logger.error(f"User action failed: User {user_name} not found")
            return {"success": False, "message": "User not found"}

        if len(user["questions"]) >= 1000:
            logger.warning(f"User action limited: {user_name} has reached question limit")
            return {"success": False, "message": "No more questions available"}

        difficulty = min(1 + len(user["questions"]) // 100, 3)
        operations = ["+", "-", "*", "/"]
        if difficulty == 2:
            operations.extend(["**"])
        elif difficulty == 3:
            operations.extend(["%", "//"])

        max_num = 50 * difficulty
        while True:
            num1 = random.randint(1, max_num)
            num2 = random.randint(1, max_num // 2) if difficulty < 3 else random.randint(1, max_num)
            operation = random.choice(operations)

            if operation in ["/", "//", "%"]:
                if num2 == 0:
                    continue
                if operation == "/":
                    num1 = num2 * random.randint(1, 10)
                elif operation == "//":
                    num1 = num2 * random.randint(1, 5)
                elif operation == "%":
                    num1 = num2 * random.randint(1, 3) + random.randint(1, num2 - 1)

            question = f"{num1} {operation} {num2}"
            question_id = f"q{len(user['questions']) + 1}"

            if any(q == question for q in user["questions"].values()):
                continue

            try:
                correct_answer = eval(question)
                if isinstance(correct_answer, float) and correct_answer.is_integer():
                    correct_answer = int(correct_answer)
            except (ZeroDivisionError, SyntaxError, NameError, OverflowError) as e:
                logger.error(f"Invalid question generated for {user_name}: {question}, Error: {str(e)}")
                continue

            user["questions"][question_id] = question
            self.save_users(self.users)
            logger.info(f"User action: {user_name} generated question {question_id}: {question}")
            return {"success": True, "question_id": question_id, "question": question, "correct_answer": correct_answer}

    def check_answer(self, user_name: str, question_id: str, user_answer: float) -> Dict[str, Any]:
        user = self.find_user(user_name)
        if not user:
            logger.error(f"User action failed: User {user_name} not found")
            return {"success": False, "message": "User not found"}

        if question_id not in user["questions"]:
            logger.error(f"User action failed: Question {question_id} not found for {user_name}")
            return {"success": False, "message": "Question not found"}

        question_text = user["questions"][question_id]
        try:
            correct_answer = eval(question_text)
            if isinstance(correct_answer, float) and correct_answer.is_integer():
                correct_answer = int(correct_answer)
        except (ZeroDivisionError, SyntaxError, NameError, OverflowError) as e:
            logger.error(f"User action failed: Error calculating answer for question '{question_text}': {str(e)}")
            return {"success": False, "message": "Invalid question format"}

        points_to_add = 10 + (len(user["questions"]) // 100) * 5
        if user.get("double_points_active", False):
            points_to_add *= 2
            user["double_points_active"] = False
            logger.info(f"User action: Double points activated for {user_name}")

        is_correct = abs(float(user_answer) - correct_answer) < 0.001 if isinstance(correct_answer,
                                                                                    float) else user_answer == correct_answer
        if is_correct:
            user["points"] += points_to_add
            logger.info(f"User action: Correct answer for {user_name}. New points: {user['points']}")
        else:
            user["points"] = max(0, user["points"] - 5 - (len(user["questions"]) // 100))
            logger.info(f"User action: Wrong answer for {user_name}. New points: {user['points']}")

        user["answers"][question_id] = {"answer": user_answer, "correct": is_correct}
        self.save_users(self.users)

        return {
            "success": True,
            "message": "Answer checked",
            "question": question_text,
            "correct_answer": correct_answer,
            "user_answer": user_answer,
            "is_correct": is_correct
        }

    def get_user_stats(self, user_name: str) -> Dict[str, Any]:
        user = self.find_user(user_name)
        if not user:
            logger.error(f"User action failed: User {user_name} not found")
            return {"success": False, "message": "User not found"}

        stats = {
            "name": user["name"],
            "points": user["points"],
            "items": user["items"],
            "questions_answered": len(user["answers"]),
            "correct_answers": sum(1 for ans in user["answers"].values() if ans.get("correct", False)),
            "double_points_active": user["double_points_active"],
            "total_questions": len(user["questions"])
        }
        logger.info(f"User action: Retrieved stats for {user_name}")
        return {"success": True, "stats": stats}

    def reset_user_progress(self, user_name: str) -> Dict[str, Any]:
        user = self.find_user(user_name)
        if not user:
            logger.error(f"User action failed: User {user_name} not found")
            return {"success": False, "message": "User not found"}

        user["points"] = 0
        user["items"] = {"Hint": 0, "Double Points": 0}
        user["questions"] = {}
        user["answers"] = {}
        user["double_points_active"] = False
        self.save_users(self.users)
        logger.info(f"User action: Reset progress for {user_name}")
        return {"success": True, "message": f"Progress reset for {user_name}"}


if __name__ == "__main__":
    game = MathQuizGame()
    response = game.generate_math_question("Akbar")
    if response["success"]:
        print(game.check_answer("Akbar", response["question_id"], 10.0))
    print(game.get_user_stats("Akbar"))
    print(game.reset_user_progress("Akbar"))