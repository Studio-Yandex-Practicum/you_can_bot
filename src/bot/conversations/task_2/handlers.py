from telegram.ext import (
    CallbackQueryHandler,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    filters,
)

from conversations.task_2.callback_funcs import (
    CHOOSING,
    cancel,
    show_start_of_task_2,
    start_question,
    update_question,
)
from conversations.task_2.keyboards import (
    CANCEL_COMMAND,
    TEXT_ENTRY_POINT_BUTTON_FOR_TASK_2,
)


task_2_handler: ConversationHandler = ConversationHandler(
    entry_points=[
        MessageHandler(
            filters.Regex(TEXT_ENTRY_POINT_BUTTON_FOR_TASK_2), show_start_of_task_2
        ),
    ],
    states={
        CHOOSING: [
            CallbackQueryHandler(start_question, pattern=r"^Далее$"),
            CallbackQueryHandler(update_question, pattern=r"^(а|б)$"),
        ]
    },
    fallbacks=[CommandHandler(CANCEL_COMMAND, cancel)],
)
