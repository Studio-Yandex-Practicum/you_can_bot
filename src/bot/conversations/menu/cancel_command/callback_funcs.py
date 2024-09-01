import logging
from typing import Optional

from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler

import conversations.menu.cancel_command.templates as templates
from conversations.general.decorators import TASK_EXECUTION

_LOGGER = logging.getLogger(__name__)


async def cancel_current_conversation(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> Optional[int]:
    """Обрабатывает команду /cancel, отменяя текущий активный диалог."""
    current_conversation = context.user_data.get("current_conversation")

    _LOGGER.info(
        "Пользователь %d использовал команду /cancel для %s",
        update.effective_chat.id,
        current_conversation,
    )

    if current_conversation == TASK_EXECUTION:
        message = templates.TASK_CANCELLED_MESSAGE
    else:
        message = templates.COMMAND_CANCELLED_MESSAGE_TEMPLATE.format(
            current_conversation
        )
    await update.message.reply_text(message)

    context.user_data.clear()
    return ConversationHandler.END


async def cancel_no_active_dialog(
    update: Update, _context: ContextTypes.DEFAULT_TYPE
) -> None:
    """Обрабатывает команду /cancel, когда активный диалог отсутствует."""
    _LOGGER.info(
        "Пользователь %d использовал команду /cancel для отсутствующего диалога",
        update.effective_chat.id,
    )
    await update.message.reply_text(templates.NO_ACTIVE_TASKS_MESSAGE)
    return None
