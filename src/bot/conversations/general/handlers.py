from telegram.ext import CallbackQueryHandler, CommandHandler, ConversationHandler

from .callback_funcs import HELLO, cancel, show_skill_set_info, start
from .templates import SHOW_SKILL_SET_INFO, START

acquaintance_handler: ConversationHandler = ConversationHandler(
    entry_points=[CommandHandler(START, start)],
    states={
        HELLO: [
            CallbackQueryHandler(
                show_skill_set_info, pattern=f"^{SHOW_SKILL_SET_INFO}$"
            ),
        ],
    },
    fallbacks=[CallbackQueryHandler(cancel)],
)
