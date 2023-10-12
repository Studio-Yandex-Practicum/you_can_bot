from telegram.ext import (
    CallbackQueryHandler,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    filters,
)

from conversations.task_3.callback_funcs import (
    CHOOSING,
    cancel,
    show_start_of_task_3,
    start_question,
    update_question,
)
from conversations.task_3.keyboards import (
    CANCEL_COMMAND,
    TEXT_ENTRY_POINT_BUTTON_FOR_TASK_3,
)

task_3_handler: ConversationHandler = ConversationHandler(
    entry_points=[
        MessageHandler(
            filters.Regex(TEXT_ENTRY_POINT_BUTTON_FOR_TASK_3), show_start_of_task_3
        ),
        CallbackQueryHandler(show_start_of_task_3, r"^start_task_3$"),
    ],
    states={
        CHOOSING: [
            CallbackQueryHandler(start_question, pattern=r"^Далее$"),
            CallbackQueryHandler(update_question, pattern=r"^(а|б)$"),
        ]
    },
    fallbacks=[CommandHandler(CANCEL_COMMAND, cancel)],
)
