import re

from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes, ConversationHandler

import internal_requests.service as api_service
from conversations.task_1.keyboards import (
    GO_TO_TASK_2_KEYBOARD,
    START_TASK_1_KEYBOARD,
    get_inline_keyboard,
)
from conversations.task_1.handlers import start_task_1
from conversations.task_2.handlers import show_start_of_task_2

from conversations.task_1.templates import (
    CANCEL_TEXT,
    END_TASK_1_TEXT,
    SCORES,
    START_TASK_1_TEXT,
)
from internal_requests.service import get_user_task_status_by_number, get_messages_with_results
from internal_requests.entities import Answer


async def show_done_tasks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    task_number = query.data.split('_')[-1]
    task_results = await get_messages_with_results(query.message.chat.id, task_number)
    for result in task_results:
        await update.callback_query.message.reply_text(text=result.content, parse_mode='html')
    # return task_results[0].content
    # return task_results
    # task_status = await get_user_task_status_by_number(task_number, query.message.chat.id)
    # print(task_status, '===============================')
    # print(query, '-------------------------------------')


async def show_undone_tasks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    task_number = query.data.split('_')[-1]
    if task_number == 1:
        await start_task_1(update, context)
    else:
        await show_start_of_task_2(update, context)

