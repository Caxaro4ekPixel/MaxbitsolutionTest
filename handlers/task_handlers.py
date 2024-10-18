from pyrogram import Client
from pyrogram.types import Message
from services.user_service import check_user_in_db
from services.task_service import create_task
from states import TaskCreationState
from database import get_db
from sqlalchemy.orm import Session
from typing import Dict

from state_manager import set_user_state, clear_user_state, main_menu


async def new_task_handler(client: Client, message: Message):
    user_id = message.from_user.id
    db: Session = next(get_db())
    user = check_user_in_db(db, user_id)
    if not user:
        await message.reply("Сначала зарегистрируйтесь, используя команду /start.")
        return

    set_user_state(user_id, TaskCreationState.ENTERING_TITLE)
    await message.reply("Введите название задачи:")


async def task_title_handler(client: Client, message: Message, state_info: Dict):
    user_id = message.from_user.id
    title = message.text.strip()
    state_info['data']['title'] = title
    set_user_state(user_id, TaskCreationState.ENTERING_DESCRIPTION, state_info['data'])
    await message.reply("Введите описание задачи или отправьте 'Пропустить':")


async def task_description_handler(client: Client, message: Message, state_info: Dict):
    user_id = message.from_user.id
    description = message.text.strip()
    if description.lower() == 'пропустить':
        description = None
    data = state_info['data']
    title = data['title']
    db: Session = next(get_db())
    user = check_user_in_db(db, user_id)
    create_task(db, user_id=user.id, title=title, description=description)
    clear_user_state(user_id)
    await message.reply(f"Задача '{title}' создана.", reply_markup=main_menu())
