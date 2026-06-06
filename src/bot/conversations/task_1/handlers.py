from conversations.task_1.callback_funcs import TaskOneConversation
from conversations.tasks.keyboards import CHOICES_SIX_LETTERS

TASK_ONE_NUMBER = 1
TASK_ONE_NUM_OF_QUESTIONS = 10
TASK_ONE_DESCRIPTION = (
    "Далее будет 10 вопросов, в каждом — шесть утверждений (А–Е).\n\n"
    "Распредели их по привлекательности: нажимай буквы по порядку —"
    " самое привлекательное первым, самое непривлекательное последним."
    " Буквы заполнят слоты от 1️⃣ до 6️⃣.\n\n"
    "Ошибся? Нажми на слот, чтобы убрать оттуда букву,"
    " или нажми ↩️ Шаг назад. Когда все шесть слотов заполнены —"
    " нажми ✅ Готово, чтобы перейти к следующему вопросу."
)
TASK_ONE_RESULT_INTRO = "<b>У тебя склонность к:</b>"
TASK_ONE_DATA = {
    "task_number": TASK_ONE_NUMBER,
    "number_of_questions": TASK_ONE_NUM_OF_QUESTIONS,
    "description": TASK_ONE_DESCRIPTION,
    "choices": CHOICES_SIX_LETTERS,
    "result_intro": TASK_ONE_RESULT_INTRO,
}

task_one = TaskOneConversation(**TASK_ONE_DATA)
task_one_conv = task_one.add_handlers()
