from telegram.ext import CallbackQueryHandler, CommandHandler, ConversationHandler

from .callback_funcs import HELLO, cancel, start, start_acquaintance
from .templates import START, START_ACQUAINTANCE

acquaintance_handler: ConversationHandler = ConversationHandler(
    entry_points=[CommandHandler(START, start)],
    states={
        HELLO: [
            CallbackQueryHandler(start_acquaintance, pattern=f"^{START_ACQUAINTANCE}$"),
        ],
    },
    fallbacks=[CallbackQueryHandler(cancel)],
)
