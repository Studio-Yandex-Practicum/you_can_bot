from conversations.tasks.base import OneQuestionConversation

TASK_FIVE_NUMBER = 5
TASK_FIVE_NUM_OF_QUESTIONS = 1
TASK_FIVE_RESULT_INTRO = (
    "Отлично! Ответ успешно сохранён, результаты этого задания"
    " озвучит психолог на консультации. Продолжим?"
)

TASK_FIVE_DATA = {
    "task_number": TASK_FIVE_NUMBER,
    "number_of_questions": TASK_FIVE_NUM_OF_QUESTIONS,
    "description": "",
    "choices": "",
    "result_intro": TASK_FIVE_RESULT_INTRO,
}


task_five = OneQuestionConversation(**TASK_FIVE_DATA)
task_five_handler = task_five.add_handlers()
