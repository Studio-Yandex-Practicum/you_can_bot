from telegram.ext import (
    CallbackQueryHandler,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    filters,
)

from conversations.task_8.callback_funcs import (
    CHOOSING,
    cancel,
    show_start_of_task_8,
    start_question,
    update_question,
)
from conversations.task_8.keyboards import (
    CANCEL_COMMAND,
    TEXT_ENTRY_POINT_BUTTON_FOR_TASK_8,
)

task_8_handler: ConversationHandler = ConversationHandler(
    entry_points=[
        MessageHandler(
            filters.Regex(TEXT_ENTRY_POINT_BUTTON_FOR_TASK_8), show_start_of_task_8
        ),
        CallbackQueryHandler(show_start_of_task_8, r"^start_task_8$"),
    ],
    states={
        CHOOSING: [
            CallbackQueryHandler(start_question, pattern=r"^Далее$"),
            CallbackQueryHandler(update_question, pattern=r"^(а|б)$"),
        ]
    },
    fallbacks=[CommandHandler(CANCEL_COMMAND, cancel)],
)
