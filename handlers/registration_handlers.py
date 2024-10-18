from pyrogram import Client
from pyrogram.types import Message
from services.user_service import register_user_in_db, check_user_in_db, get_user_by_login
from states import RegistrationState
from database import get_db
from sqlalchemy.orm import Session
from typing import Dict

from state_manager import set_user_state, clear_user_state, main_menu


async def start_command_handler(client: Client, message: Message):
    db: Session = next(get_db())
    telegram_id = message.from_user.id
    user = check_user_in_db(db, telegram_id)

    if user:
        await message.reply(f"Вы уже зарегистрированы как {user.name}.", reply_markup=main_menu())
    else:
        set_user_state(telegram_id, RegistrationState.ENTERING_NAME)
        await message.reply("Привет! Пожалуйста, введите ваше имя:")


async def registration_name_handler(client: Client, message: Message, state_info: Dict):
    user_id = message.from_user.id
    name = message.text.strip()
    state_info['data']['name'] = name
    set_user_state(user_id, RegistrationState.ENTERING_LOGIN, state_info['data'])
    await message.reply("Пожалуйста, выберите уникальный логин:")


async def registration_login_handler(client: Client, message: Message, state_info: Dict):
    user_id = message.from_user.id
    login = message.text.strip()
    db: Session = next(get_db())
    existing_user = get_user_by_login(db, login)
    if existing_user:
        await message.reply("Этот логин уже занят, пожалуйста, выберите другой.")
    else:
        data = state_info['data']
        name = data['name']
        telegram_id = user_id
        register_user_in_db(db, name, login, telegram_id)
        clear_user_state(user_id)
        await message.reply(f"Регистрация завершена! Добро пожаловать, {name}!", reply_markup=main_menu())
