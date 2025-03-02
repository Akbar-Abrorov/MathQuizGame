import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='math_quiz_game.log'
)

logger = logging.getLogger('MathQuizGame')