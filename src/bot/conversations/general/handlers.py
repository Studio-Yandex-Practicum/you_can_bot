from telegram.ext import CallbackQueryHandler, CommandHandler, ConversationHandler

from conversations.general.callback_funcs import HELLO, show_skill_set_info, start
from conversations.general.templates import SHOW_SKILL_SET_INFO, START
from conversations.menu.handlers import cancel_handler

acquaintance_handler: ConversationHandler = ConversationHandler(
    entry_points=[CommandHandler(START, start)],
    states={
        HELLO: [
            CallbackQueryHandler(
                show_skill_set_info, pattern=f"^{SHOW_SKILL_SET_INFO}$"
            ),
        ],
    },
    fallbacks=[cancel_handler],
)
