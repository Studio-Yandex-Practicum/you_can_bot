from telegram.ext import CallbackQueryHandler, ConversationHandler

from conversations.menu.cancel_command.handlers import cancel_handler
from conversations.task_8.callback_funcs import (
    END_STAGE,
    FINAL_STATE,
    STAGE_1,
    STAGE_2,
    STAGE_3,
    TASK_DESCRIPTION_STATE,
    clear_conversation_status_of_tasks_command,
    handle_answer_on_stage_1,
    handle_answer_on_stage_2,
    handle_answer_on_stage_3,
    send_final_message,
    send_first_question,
    send_next_stage_2_message,
    send_next_stage_3_message,
    show_result,
    show_start_of_task_8,
)

task_8_conv: ConversationHandler = ConversationHandler(
    entry_points=[
        CallbackQueryHandler(show_start_of_task_8, r"^start_task_8$"),
        CallbackQueryHandler(
            clear_conversation_status_of_tasks_command,
            pattern=r"^start_task_from_command_8$",
        ),
    ],
    states={
        TASK_DESCRIPTION_STATE: [
            CallbackQueryHandler(send_first_question, pattern=r"^Далее$"),
        ],
        STAGE_1: [
            CallbackQueryHandler(handle_answer_on_stage_1, pattern=r"^(а|б)$"),
        ],
        STAGE_2: [
            CallbackQueryHandler(handle_answer_on_stage_2, pattern=r"^(а|б)$"),
        ],
        STAGE_3: [
            CallbackQueryHandler(handle_answer_on_stage_3, pattern=r"^(а|б)$"),
        ],
        END_STAGE: [
            CallbackQueryHandler(send_next_stage_2_message, pattern=r"^next_stage_2$"),
            CallbackQueryHandler(send_next_stage_3_message, pattern=r"^next_stage_3$"),
            CallbackQueryHandler(show_result, pattern=r"^finish_task_8$"),
        ],
        FINAL_STATE: [
            CallbackQueryHandler(send_final_message, pattern=r"^further_actions$"),
        ],
    },
    fallbacks=[cancel_handler],
    map_to_parent={ConversationHandler.END: ConversationHandler.END},
)
