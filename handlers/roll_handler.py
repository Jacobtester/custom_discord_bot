#roll_handler.py
import random


async def roll_command() -> str:
    return str(random.randint(1, 6))