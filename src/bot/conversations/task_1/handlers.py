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
    cancel,
    get_answer_question,
    get_start_question,
    start_task_1,
)

task_1_handler = ConversationHandler(
    entry_points=[
        MessageHandler(filters.Regex(FIRST_TASK_BUTTON_LABEL), start_task_1),
        CallbackQueryHandler(start_task_1, r"^start_task_1$"),
    ],
    states={
        CHOOSING: [
            CallbackQueryHandler(get_start_question, pattern=r"^Далее$"),
            CallbackQueryHandler(get_answer_question, pattern=f"^([{CHOICES}])$"),
        ],
    },
    fallbacks=[CommandHandler("cancel", cancel)],
)
