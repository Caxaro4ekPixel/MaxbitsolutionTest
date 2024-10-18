from pyrogram.types import ReplyKeyboardMarkup, KeyboardButton
from typing import Dict, Optional
from enum import Enum

user_states: Dict[int, Dict] = {}


def set_user_state(user_id: int, state: Enum, data: Optional[Dict] = None) -> None:
    user_states[user_id] = {'state': state, 'data': data or {}}


def get_user_state(user_id: int) -> Optional[Dict]:
    return user_states.get(user_id)


def clear_user_state(user_id: int) -> None:
    user_states.pop(user_id, None)


def main_menu() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        [
            [KeyboardButton("/newtask"), KeyboardButton("/mytasks")],
            [KeyboardButton("/help")]
        ],
        resize_keyboard=True
    )
