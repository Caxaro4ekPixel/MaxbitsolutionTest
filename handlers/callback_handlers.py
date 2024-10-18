from pyrogram import Client
from pyrogram import enums
from pyrogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from services.task_service import get_task_by_id, delete_task, mark_task_done
from database import get_db
from sqlalchemy.orm import Session


async def task_callback_handler(client: Client, callback_query: CallbackQuery):
    task_id = int(callback_query.data.split(":")[1])
    db: Session = next(get_db())
    task = get_task_by_id(db, task_id)
    if not task:
        await callback_query.message.edit_text("Задача не найдена.", reply_markup=None)
        return

    task_info = (
        f"**Задача:** {task.title}\n"
        f"**Описание:** {task.description or 'Нет описания'}\n"
        f"**Дата создания:** {task.created_at.strftime('%Y/%m/%d %H:%M:%S')}\n"
        f"**Статус:** {'Завершена' if task.is_done else 'В процессе'}"
    )

    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("Удалить", callback_data=f"delete:{task.id}"),
                InlineKeyboardButton("Выполнено!", callback_data=f"done:{task.id}")
            ]
        ]
    )

    await callback_query.message.edit_text(
        task_info,
        reply_markup=keyboard,
        parse_mode=enums.ParseMode.MARKDOWN
    )


async def delete_task_callback_handler(client: Client, callback_query: CallbackQuery):
    task_id = int(callback_query.data.split(":")[1])
    db: Session = next(get_db())
    delete_task(db, task_id)
    await callback_query.message.edit_text("Задача удалена.", reply_markup=None)


async def mark_task_done_callback_handler(client: Client, callback_query: CallbackQuery):
    task_id = int(callback_query.data.split(":")[1])
    db: Session = next(get_db())
    mark_task_done(db, task_id)
    await callback_query.message.edit_text("Задача выполнена!", reply_markup=None)
