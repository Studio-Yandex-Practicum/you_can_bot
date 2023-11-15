from telegram.ext import CallbackQueryHandler, ConversationHandler

from conversations.task_8.callback_funcs import (
    CHOOSING,
    NEXT,
    show_start_of_task_8,
    start_question,
    update_question,
)

task_8_handler: ConversationHandler = ConversationHandler(
    entry_points=[
        CallbackQueryHandler(show_start_of_task_8, r"^start_task_8$"),
    ],
    states={
        NEXT: [
            CallbackQueryHandler(start_question, pattern=r"^Далее$"),
        ],
        CHOOSING: [
            CallbackQueryHandler(update_question, pattern=r"^(а|б)$"),
        ],
    },
    fallbacks=[],
)