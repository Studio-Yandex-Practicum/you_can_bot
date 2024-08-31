from telegram.ext import (
    CallbackQueryHandler,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    filters,
)

import conversations.menu.callback_funcs as callback_funcs
from conversations.general.decorators import handle_prohibited_command
from conversations.menu.cancel_command.handlers import cancel_handler
from conversations.menu.templates import (
    TASKS_STATE,
    WAITING_FOR_CONFIRMATION_STATE,
    WAITING_FOR_QUESTION_STATE,
)
from conversations.task_1.handlers import task_one_conv
from conversations.task_2.handlers import task_two_conv
from conversations.task_3.handlers import task_three_conv
from conversations.task_4.handlers import task_four_conv
from conversations.task_5.handlers import task_five_conv
from conversations.task_6.handlers import task_six_conv
from conversations.task_7.handlers import task_seven_conv
from conversations.task_8.handlers import task_8_conv

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
            task_one_conv,
            task_two_conv,
            task_three_conv,
            task_four_conv,
            task_five_conv,
            task_six_conv,
            task_seven_conv,
            task_8_conv,
        ]
    },
    fallbacks=[
        cancel_handler,
        CommandHandler("tasks", handle_prohibited_command),
    ],
)
# /ask
entry_point_to_ask_handler = CommandHandler("ask", callback_funcs.suggest_ask_question)
ask_question_handler = ConversationHandler(
    entry_points=[entry_point_to_ask_handler],
    states={
        WAITING_FOR_QUESTION_STATE: [
            MessageHandler(
                filters=filters.TEXT & (~filters.COMMAND),
                callback=callback_funcs.handle_user_question,
            )
        ],
        WAITING_FOR_CONFIRMATION_STATE: [
            MessageHandler(
                filters=filters.UpdateType.EDITED_MESSAGE,
                callback=callback_funcs.handle_user_question_edit,
            ),
        ],
    },
    fallbacks=[
        CallbackQueryHandler(
            callback_funcs.confirm_saving_question, pattern=r"^agree_question$"
        ),
        CallbackQueryHandler(
            callback_funcs.cancel_save_question, pattern=r"^cancel_question$"
        ),
        cancel_handler,
        CommandHandler("ask", handle_prohibited_command),
    ],
)
# /info
info_handler = CommandHandler("info", callback_funcs.show_url)
