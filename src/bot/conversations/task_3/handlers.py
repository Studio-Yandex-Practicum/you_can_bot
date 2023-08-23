from telegram.ext import CommandHandler, ConversationHandler, MessageHandler, filters

from conversations.task_3.callback_funcs import (
    DESCRIPTION_MARKER,
    FIRST_QUESTION_MARKER,
    OTHER_QUESTIONS_MARKER,
    cancel,
    show_question,
    show_result,
    show_start_of_test_3
)
from conversations.task_3.keyboards import (
    CANCEL_COMMAND,
    TEXT_ENTRY_POINT_BUTTON_FOR_TASK_3
)


FILTER = filters.Regex("^(а|б)$")

task_3_handler: ConversationHandler = ConversationHandler(
    entry_points=[
        MessageHandler(
            filters.Regex(TEXT_ENTRY_POINT_BUTTON_FOR_TASK_3), show_start_of_test_3
        )
    ],
    states={
        FIRST_QUESTION_MARKER: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, show_question)
        ],
        OTHER_QUESTIONS_MARKER: [MessageHandler(FILTER, show_question)],
        DESCRIPTION_MARKER: [MessageHandler(FILTER, show_result)],
    },
    fallbacks=[CommandHandler(CANCEL_COMMAND, cancel)],
)
