import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('math_quiz_game.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("Math_Game")