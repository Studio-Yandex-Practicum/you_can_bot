import re

from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

from conversations.tasks.base import CHOOSING, BaseTaskConversation
from conversations.tasks.keyboards import get_default_inline_keyboard
from internal_requests import service as api_service
from internal_requests.entities import Answer

LABEL_PATTERN = r"\[([А-Я])\]"
IDX_IN_STR = 4
MAX_SCORE = 5
SCORES = {
    0: " 0️⃣ баллов",
    1: " 1️⃣ балл",
    2: " 2️⃣ баллa",
    3: " 3️⃣ баллa",
    4: " 4️⃣ баллa",
    5: " 5️⃣ баллов",
}


class TaskOneConversation(BaseTaskConversation):
    """
    Класс для обработки диалогов в Задании 1. В классе переопределяется метод
    отображения вопросов и метод обработки ответов пользователя.
    """

    async def show_question(
        self,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
        question_number: int = 1,
    ) -> None:
        """
        Выводит вопросы в Задании 1: текст вопроса + клавиатура с исходными
        вариантами ответов: А Б В Г Д Е.
        """
        if question_number == 1:
            await update.callback_query.edit_message_reply_markup()
        context.user_data["picked_choices"] = ""
        messages = await api_service.get_messages_with_question(
            task_number=self.task_number,
            question_number=question_number,
        )
        await update.effective_message.reply_text(
            text=messages[0].content,
            reply_markup=get_default_inline_keyboard(self.choices),
            parse_mode=ParseMode.HTML,
        )

    async def handle_user_answer(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> int:
        """
        Обрабатывает ответ пользователя на вопрос: при нажатии на вариант
        ответа, записывает этот вариант и убирает его из списка вариантов на
        клавиатуре. Для контроля вариантов ответа используется переменная
        picked_choices.
        """
        choice = update.callback_query.data
        context.user_data["picked_choices"] += choice
        picked_choices = context.user_data.get("picked_choices")
        message = update.effective_message
        await update.effective_message.edit_text(
            self._get_question_text(message.text_html.split("\n\n"), picked_choices),
            reply_markup=get_default_inline_keyboard(self.choices, picked_choices),
            parse_mode=ParseMode.HTML,
        )
        current_question = context.user_data.get("current_question")
        if len(picked_choices) == len(self.choices):
            await self._save_answer(
                message.chat_id,
                current_question,
                picked_choices,
            )
            if current_question == self.number_of_questions:
                state = await self.show_result(update, context)
                return state
            context.user_data["current_question"] += 1
            await self.show_question(
                update, context, context.user_data.get("current_question")
            )
        return CHOOSING

    async def _save_answer(self, user_id, current_question, picked_choices):
        """Сохраняет ответ пользователя в БД."""
        answers = ""
        for label in self.choices:
            answers += str(MAX_SCORE - picked_choices.index(label))
        await api_service.create_answer(
            Answer(
                telegram_id=user_id,
                task_number=self.task_number,
                number=current_question,
                content=answers,
            )
        )

    @staticmethod
    def _get_question_text(message_text, picked_choices: str = "") -> str:
        text = f"{message_text[0]}\n\n"
        for string in message_text[1:]:
            text += f"{string}"
            if re.search(LABEL_PATTERN, string).group(1) == picked_choices[-1]:
                text += (
                    f" — {SCORES[MAX_SCORE - picked_choices.index(string[IDX_IN_STR])]}"
                )
            text += "\n\n"
        return text
