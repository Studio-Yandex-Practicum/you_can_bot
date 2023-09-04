from telegram.ext import CommandHandler, ConversationHandler, MessageHandler, filters

from conversations.general.callback_funcs import (
    HELLO,
    NAME,
    START,
    cancel,
    name,
    start,
    start_acquaintance,
    start_skill_sets,
)
from conversations.general.templates import HELLO_BUTTON_LABEL, START_BUTTON_LABEL

acquaintance_handler: ConversationHandler = ConversationHandler(
    entry_points=[CommandHandler("start", start)],
    states={
        HELLO: [MessageHandler(filters.Regex(HELLO_BUTTON_LABEL), start_acquaintance)],
        NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, name)],
        START: [MessageHandler(filters.Regex(START_BUTTON_LABEL), start_skill_sets)],
    },
    fallbacks=[CommandHandler("cancel", cancel)],
)
