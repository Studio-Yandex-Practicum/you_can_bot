from telegram.ext import CallbackQueryHandler, CommandHandler, ConversationHandler

from .callback_funcs import HELLO, cancel, start, start_acquaintance, start_skill_sets
from .templates import START, START_ACQUAINTANCE, START_SKILL_SETS

acquaintance_handler: ConversationHandler = ConversationHandler(
    entry_points=[CommandHandler(START, start)],
    states={
        HELLO: [
            CallbackQueryHandler(start_acquaintance, pattern=f"^{START_ACQUAINTANCE}$"),
            CallbackQueryHandler(start_skill_sets, pattern=f"^{START_SKILL_SETS}$"),
        ],
    },
    fallbacks=[CallbackQueryHandler(cancel)],
)
