from telegram.ext import CallbackQueryHandler, ConversationHandler

from conversations.task_8.callback_funcs import (
    FINAL_STATE,
    END_STAGE,
    STAGE_1,
    STAGE_2,
    STAGE_3,
    TASK_DESCRIPTION_STATE,
    handle_answer_on_stage_1,
    handle_answer_on_stage_2,
    handle_answer_on_stage_3,
    send_final_message,
    send_first_question,
    send_next_stage_2_message,
    send_next_stage_3_message,
    show_result,
    show_start_of_task_8,
    show_start_of_task_8_with_task_number,
)

task_8_handler: ConversationHandler = ConversationHandler(
    entry_points=[
        CallbackQueryHandler(show_start_of_task_8, r"^start_task_8$"),
        CallbackQueryHandler(
            show_start_of_task_8_with_task_number, r"^with_choice_start_task_8$"
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
    fallbacks=[],
)
