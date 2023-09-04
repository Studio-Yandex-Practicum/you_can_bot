from telegram.ext import (
    CallbackQueryHandler,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    filters,
)

from conversations.general.templates import FIRST_TASK_BUTTON_LABEL
from conversations.task_1.callback_funcs import (
    CHOICES,
    CHOOSING,
    button,
    cancel,
    start_task_1,
)

task_1_handler = ConversationHandler(
    entry_points=[
        MessageHandler(filters.Regex(FIRST_TASK_BUTTON_LABEL), start_task_1),
    ],
    states={
        CHOOSING: [
            MessageHandler(filters.Regex("^(Далее)$"), button),
            CallbackQueryHandler(button, pattern=f"^([{CHOICES}])$"),
        ],
    },
    fallbacks=[CommandHandler("cancel", cancel)],
)
