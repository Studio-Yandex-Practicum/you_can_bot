from telegram.ext import (
    CallbackQueryHandler,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    filters,
)

from conversations.task_3.callback_funcs import (
    DESCRIPTION_MARKER,
    FIRST_QUESTION_MARKER,
    OTHER_QUESTIONS_MARKER,
    cancel,
    show_question,
    show_result,
    show_start_of_task_3,
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
    ],
    states={
        FIRST_QUESTION_MARKER: [
            CallbackQueryHandler(show_question, pattern=r"^Далее$")
        ],
        OTHER_QUESTIONS_MARKER: [
            CallbackQueryHandler(show_question, pattern=r"^(а|б)$")
        ],
        DESCRIPTION_MARKER: [CallbackQueryHandler(show_result, pattern=r"^(а|б)$")],
    },
    fallbacks=[CommandHandler(CANCEL_COMMAND, cancel)],
)
