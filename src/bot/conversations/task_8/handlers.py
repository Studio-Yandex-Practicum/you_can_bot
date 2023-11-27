from telegram.ext import CallbackQueryHandler, ConversationHandler

from conversations.task_8.callback_funcs import (
    FINAL_STATE,
    PASSING_TEST_STATE,
    TASK_DESCRIPTION_STATE,
    send_final_message,
    show_result,
    show_start_of_task_8,
    show_start_of_task_8_with_task_number,
    start_question,
    update_question,
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
            CallbackQueryHandler(start_question, pattern=r"^Далее$"),
        ],
        PASSING_TEST_STATE: [
            CallbackQueryHandler(update_question, pattern=r"^(а|б)$"),
            CallbackQueryHandler(start_question, pattern=r"^next_stage$"),
            CallbackQueryHandler(show_result, pattern=r"^finish_task_8$"),
        ],
        FINAL_STATE: [
            CallbackQueryHandler(send_final_message, pattern=r"^further_actions$"),
        ],
    },
    fallbacks=[],
)
