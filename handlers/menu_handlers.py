from pyrogram import Client
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from services.user_service import check_user_in_db
from services.task_service import get_user_tasks
from database import get_db
from sqlalchemy.orm import Session

from state_manager import main_menu


async def view_tasks_handler(client: Client, message: Message):
    user_id = message.from_user.id
    db: Session = next(get_db())
    user = check_user_in_db(db, user_id)
    if not user:
        await message.reply("Сначала зарегистрируйтесь, используя команду /start.")
        return

    tasks = get_user_tasks(db, user.id)
    if not tasks:
        await message.reply("У вас нет задач.", reply_markup=main_menu())
        return

    buttons = [
        [InlineKeyboardButton(task.title, callback_data=f"task:{task.id}")]
        for task in tasks
    ]
    keyboard = InlineKeyboardMarkup(buttons)
    await message.reply("Ваши задачи:", reply_markup=keyboard)


async def help_command_handler(client: Client, message: Message):
    help_text = (
        "Доступные команды:\n"
        "/start - Начало работы и регистрация\n"
        "/newtask - Создать новую задачу\n"
        "/mytasks - Показать мои задачи\n"
        "/help - Показать это сообщение"
    )
    await message.reply(help_text, reply_markup=main_menu())
