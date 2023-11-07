from conversations.task_7.callback_funcs import TaskSevenConversation

TASK_SEVEN_NUMBER = 7
TASK_SEVEN_NUM_OF_QUESTIONS = 1
TAKS_SEVEN_RESULT_INTRO = (
    "Отлично! Ответ успешно сохранён, "
    "результаты этого задания озвучит психолог на консультации. Продолжим?"
)

TASK_SEVEN_DATA = {
    "task_number": TASK_SEVEN_NUMBER,
    "number_of_questions": TASK_SEVEN_NUM_OF_QUESTIONS,
    "description": "",
    "choices": "",
    "result_intro": TAKS_SEVEN_RESULT_INTRO,
}

task_seven = TaskSevenConversation(**TASK_SEVEN_DATA)
task_seven_handler = task_seven.add_handlers()
