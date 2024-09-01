from conversations.tasks.base import BaseTaskConversation
from conversations.tasks.keyboards import CHOICES_TWO_LETTERS

TASK_THREE_NUMBER = 3
TASK_THREE_NUM_OF_QUESTIONS = 42
TASK_THREE_DESCRIPTION = (
    "Сейчас тебе будут представлены 42 пары различных видов деятельности. "
    "Если бы тебе пришлось выбирать лишь одну работу из каждой пары, "
    "что бы ты предпочёл?\n\n"
)
TASK_THREE_RESULT_INTRO = "<b>Твой тип личности:</b>"
TASK_THREE_DATA = {
    "task_number": TASK_THREE_NUMBER,
    "number_of_questions": TASK_THREE_NUM_OF_QUESTIONS,
    "description": TASK_THREE_DESCRIPTION,
    "choices": CHOICES_TWO_LETTERS,
    "result_intro": TASK_THREE_RESULT_INTRO,
}
task_three = BaseTaskConversation(**TASK_THREE_DATA)
task_three_conv = task_three.add_handlers()
