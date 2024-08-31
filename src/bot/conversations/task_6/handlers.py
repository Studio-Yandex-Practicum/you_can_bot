from conversations.task_6.callback_funcs import TaskSixConversation

TASK_SIX_NUMBER = 6
TASK_SIX_NUM_OF_QUESTIONS = 3
TASK_SIX_DESCRIPTION = (
    "Сейчас тебе будет предоставлено 3 вопроса."
    " Твоя задача — написать все, что приходит в голову."
)
TASK_SIX_RESULT_INTRO = (
    "Отлично! Ответы успешно сохранены, результаты "
    "этого задания озвучит профдизайнер на консультации. Продолжим?"
)
TASK_SIX_DATA = {
    "task_number": TASK_SIX_NUMBER,
    "number_of_questions": TASK_SIX_NUM_OF_QUESTIONS,
    "description": TASK_SIX_DESCRIPTION,
    "choices": "",
    "result_intro": TASK_SIX_RESULT_INTRO,
}
task_six = TaskSixConversation(**TASK_SIX_DATA)
task_six_conv = task_six.add_handlers()
