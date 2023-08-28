from telegram.ext import CommandHandler, ConversationHandler, filters, MessageHandler

from conversations.task_4.callback_funcs import (
    cancel,
    DESCRIPTION_MARKER,
    FIRST_QUESTION_MARKER,
    OTHER_QUESTIONS_MARKER,
    show_question,
    show_result,
    show_start_of_test_4,
)
from conversations.task_4.keyboards import (
    CANCEL_COMMAND,
    TEXT_ENTRY_POINT_BUTTON_FOR_TASK_4,
)


FILTER = filters.Regex("[1-9][\uFE0F\u20E3]|[\U0001f51f]")


task_4_handler: ConversationHandler = ConversationHandler(
    entry_points=[
        MessageHandler(
            filters.Regex(TEXT_ENTRY_POINT_BUTTON_FOR_TASK_4), show_start_of_test_4
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
