from telegram.ext import CallbackQueryHandler

from conversations.mentor_registration.callback_funcs import (
    REGISTRATION_CONFIRM,
    REGISTRATION_REJECT,
    MentorRegistrationConversation,
    registration_confirmation,
)

mentor_registration_handler = MentorRegistrationConversation().add_handlers()
registration_confirmation_handler = CallbackQueryHandler(
    callback=registration_confirmation,
    pattern=rf"^({REGISTRATION_CONFIRM}|{REGISTRATION_REJECT})\.\d+$",
)
