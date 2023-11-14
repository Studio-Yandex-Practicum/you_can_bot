from telegram.ext import (
    CallbackQueryHandler,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    filters,
)

import conversations.menu.callback_funcs as callback_funcs
from conversations.menu.templates import (
    SHOW_MY_TASKS_STATE,
    TASKS_STATE,
    WAITING_FOR_QUESTION_STATE,
)

# /profile
entry_point_to_profile_handler = CommandHandler(
    "profile", callback_funcs.get_user_profile
)
profile_handler = ConversationHandler(
    entry_points=[entry_point_to_profile_handler],
    states={
        SHOW_MY_TASKS_STATE: [
            CallbackQueryHandler(
                callback_funcs.show_all_user_tasks, pattern=r"^my_tasks$"
            )
        ],
        TASKS_STATE: [
            CallbackQueryHandler(
                callback_funcs.show_done_tasks, pattern=r"^result_task_(?P<number>\d+)$"
            ),
        ],
    },
    fallbacks=[],
)
# /tasks
entry_point_to_tasks_handler = CommandHandler(
    "tasks", callback_funcs.show_all_user_tasks
)
show_all_tasks_handler = ConversationHandler(
    entry_points=[
        entry_point_to_tasks_handler,
    ],
    states={
        TASKS_STATE: [
            CallbackQueryHandler(
                callback_funcs.show_done_tasks, pattern=r"^result_task_(?P<number>\d+)$"
            ),
            CallbackQueryHandler(
                callback_funcs.finish_tasks_conversation,
                pattern=r"^start_task_(?P<number>\d+)$",
            ),
        ]
    },
    fallbacks=[],
)
# /ask
entry_point_to_ask_handler = CommandHandler("ask", callback_funcs.suggest_ask_question)
ask_question_handler = ConversationHandler(
    entry_points=[entry_point_to_ask_handler],
    states={
        WAITING_FOR_QUESTION_STATE: [
            MessageHandler(
                filters.TEXT & (~filters.COMMAND),
                callback_funcs.get_user_question,
            )
        ],
    },
    fallbacks=[
        CallbackQueryHandler(
            callback_funcs.confirm_saving_question, pattern=r"^agree_question$"
        ),
        CallbackQueryHandler(
            callback_funcs.cancel_save_question, pattern=r"^cancel_question$"
        ),
    ],
)
# /info
info_handler = CommandHandler("info", callback_funcs.show_url)
