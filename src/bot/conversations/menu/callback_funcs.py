from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

from internal_requests.service import get_messages_with_results

from .templates import PICKED_TASK


async def show_done_tasks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    task_number = query.data.split("_")[-1]
    task_results = await get_messages_with_results(query.message.chat.id, task_number)
    await update.callback_query.message.edit_text(
        text=PICKED_TASK.format(task_number=task_number), parse_mode=ParseMode.HTML
    )
    for result in task_results:
        await update.callback_query.message.reply_text(
            text=result.content, parse_mode=ParseMode.HTML
        )


async def show_undone_tasks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    task_number = int(query.data.split("_")[-1])
    await update.callback_query.message.edit_text(
        text=PICKED_TASK.format(task_number=task_number), parse_mode=ParseMode.HTML
    )
