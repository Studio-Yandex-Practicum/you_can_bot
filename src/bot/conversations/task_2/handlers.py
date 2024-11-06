from conversations.tasks.base import BaseTaskConversation
from conversations.tasks.keyboards import CHOICES_TWO_LETTERS

TASK_TWO_NUMBER = 2
TASK_TWO_NUM_OF_QUESTIONS = 70
TASK_TWO_DESCRIPTION = (
    "Ниже 70 вопросов, в каждом из них — два утверждения."
    " Выбери то продолжение, которое свойственно тебе больше всего."
    " Важно: подолгу не задумывайся над ответами!\n\n"
)
TASK_TWO_DATA = {
    "task_number": TASK_TWO_NUMBER,
    "number_of_questions": TASK_TWO_NUM_OF_QUESTIONS,
    "description": TASK_TWO_DESCRIPTION,
    "choices": CHOICES_TWO_LETTERS,
    "result_intro": "",
}
task_two = BaseTaskConversation(**TASK_TWO_DATA)
task_two_conv = task_two.add_handlers()
