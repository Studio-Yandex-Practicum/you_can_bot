from conversations.tasks.base import BaseTaskConversation
from conversations.tasks.keyboards import CHOICES_TEN_NUMBERS

TASK_FOUR_NUMBER = 4
TASK_FOUR_NUM_OF_QUESTIONS = 41
TASK_FOUR_DESCRIPTION = (
    "Насколько ты согласен с каждым из следующих утверждений? "
    "Варианты ответов:\n"
    "1 – совершенно не согласен\n"
    "10 – полностью согласен\n\n"
)
TASK_FOUR_RESULT_INTRO = "Твои ценностные ориентации: \n\n"
TASK_FOUR_DATA = {
    "task_number": TASK_FOUR_NUMBER,
    "number_of_questions": TASK_FOUR_NUM_OF_QUESTIONS,
    "description": TASK_FOUR_DESCRIPTION,
    "choices": CHOICES_TEN_NUMBERS,
    "result_intro": TASK_FOUR_RESULT_INTRO,
}
task_four = BaseTaskConversation(**TASK_FOUR_DATA)
task_four_conv = task_four.add_handlers()
