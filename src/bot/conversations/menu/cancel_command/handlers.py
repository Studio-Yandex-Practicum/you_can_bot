from telegram.ext import CommandHandler

from conversations.menu.cancel_command.callback_funcs import (
    cancel_current_conversation,
    cancel_no_active_dialog,
)

cancel_handler = CommandHandler(
    "cancel",
    cancel_current_conversation,
)
no_active_dialog_cancel_handler = CommandHandler(
    "cancel",
    cancel_no_active_dialog,
)
