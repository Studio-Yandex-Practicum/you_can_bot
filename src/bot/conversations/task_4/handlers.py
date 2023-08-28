from telegram.ext import CommandHandler, ConversationHandler, MessageHandler, filters

from callback_funcs import (
    DESCRIPTION_MARKER,
    FIRST_QUESTION_MARKER,
    OTHER_QUESTIONS_MARKER,
    cancel,
    show_question,
    show_result,
    show_start_of_test_4,
)
from keyboards import (
    CANCEL_COMMAND,
    TEXT_ENTRY_POINT_BUTTON_FOR_TASK_4,
)

FILTER = filters.Regex("^(а|б)$")

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

if __name__ == "__main__":
    import os
    from dotenv import load_dotenv
    from telegram.ext import Application
    from telegram import Update
    load_dotenv()
    TOKEN = os.getenv('TOKEN')
    application = Application.builder().token(TOKEN).build()
    application.add_handler(task_4_handler)
    application.run_polling(allowed_updates=Update.ALL_TYPES)
