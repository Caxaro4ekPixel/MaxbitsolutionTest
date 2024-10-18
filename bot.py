from pyrogram import Client, filters
from pyrogram.types import Message, CallbackQuery
from config import API_ID, API_HASH, BOT_TOKEN
from states import RegistrationState, TaskCreationState
from handlers import (
    start_command_handler, registration_name_handler, registration_login_handler,
    new_task_handler, task_title_handler, task_description_handler,
    view_tasks_handler, help_command_handler,
    task_callback_handler, delete_task_callback_handler, mark_task_done_callback_handler
)
from state_manager import get_user_state, main_menu
from typing import Dict
import logging

logging.basicConfig(level=logging.INFO)

user_states: Dict[int, Dict] = {}

app = Client("task_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)


@app.on_message(filters.command("start"))
async def start(client: Client, message: Message):
    await start_command_handler(client, message)


@app.on_message(filters.command("newtask"))
async def new_task(client: Client, message: Message):
    await new_task_handler(client, message)


@app.on_message(filters.command("mytasks"))
async def view_tasks(client: Client, message: Message):
    await view_tasks_handler(client, message)


@app.on_message(filters.command("help"))
async def help_command(client: Client, message: Message):
    await help_command_handler(client, message)


@app.on_message(filters.private & filters.text & ~filters.regex('^/'))
async def text_message_handler(client: Client, message: Message):
    user_id = message.from_user.id
    state_info = get_user_state(user_id)

    if state_info:
        state = state_info['state']

        if state == RegistrationState.ENTERING_NAME:
            await registration_name_handler(client, message, state_info)
        elif state == RegistrationState.ENTERING_LOGIN:
            await registration_login_handler(client, message, state_info)
        elif state == TaskCreationState.ENTERING_TITLE:
            await task_title_handler(client, message, state_info)
        elif state == TaskCreationState.ENTERING_DESCRIPTION:
            await task_description_handler(client, message, state_info)
        else:
            await message.reply("Неизвестное состояние. Пожалуйста, используйте меню.", reply_markup=main_menu())
    else:
        await message.reply("Пожалуйста, используйте меню.", reply_markup=main_menu())


@app.on_callback_query(filters.regex(r"^task:\d+$"))
async def task_callback(client: Client, callback_query: CallbackQuery):
    await task_callback_handler(client, callback_query)


@app.on_callback_query(filters.regex(r"^delete:\d+$"))
async def delete_task_callback(client: Client, callback_query: CallbackQuery):
    await delete_task_callback_handler(client, callback_query)


@app.on_callback_query(filters.regex(r"^done:\d+$"))
async def mark_task_done_callback(client: Client, callback_query: CallbackQuery):
    await mark_task_done_callback_handler(client, callback_query)


if __name__ == "__main__":
    app.run()
