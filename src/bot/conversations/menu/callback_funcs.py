from telegram import Update
from telegram.ext import ContextTypes

from internal_requests.service import get_messages_with_results

from .templates import TASKS


async def show_done_tasks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    task_number = query.data.split("_")[-1]
    task_results = await get_messages_with_results(query.message.chat.id, task_number)
    for result in task_results:
        await update.callback_query.message.reply_text(
            text=result.content, parse_mode="html"
        )


async def show_undone_tasks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    task_number = int(query.data.split("_")[-1])
    if task_number in TASKS:
        await TASKS[task_number](update, context)
    else:
        # Заглушка, пока не появятся функции для всез заданий
        print("Такого задания пока что нет")
