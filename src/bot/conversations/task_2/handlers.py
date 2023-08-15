from telegram import Update
from telegram.ext import (
    CommandHandler, ConversationHandler, filters, MessageHandler
)

from callback_funcs import (
    cancel, description, DESCRIPTION_MARKER, FIRST_QUESTION_MARKER,
    OTHER_QUESTIONS_MARKER, show_question, start
)
from keyboards import CANCEL_COMMAND, MAGIC_WORD_FOR_START_THIS_HANDLER, NEXT


FILTER = filters.Regex("^(а|б)$")


task_2_handler = ConversationHandler(
        entry_points=[
            MessageHandler(
                filters.Regex(MAGIC_WORD_FOR_START_THIS_HANDLER),
                start
            )
        ],
        states={
            FIRST_QUESTION_MARKER: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, show_question)
            ],
            OTHER_QUESTIONS_MARKER: [MessageHandler(FILTER, show_question)],
            DESCRIPTION_MARKER: [MessageHandler(FILTER, description)]
        },
        fallbacks=[CommandHandler(CANCEL_COMMAND, cancel)],
    )


if __name__ == "__main__":
    import os
    from dotenv import load_dotenv
    from telegram.ext import Application
    load_dotenv()
    TOKEN = os.getenv('TOKEN')
    application = Application.builder().token(TOKEN).build()
    application.add_handler(task_2_handler)
    application.run_polling(allowed_updates=Update.ALL_TYPES)
