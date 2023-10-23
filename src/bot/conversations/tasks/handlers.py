import re

from dataclasses import dataclass

from telegram import Update
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode
from telegram.ext import (
    CallbackQueryHandler,
    CommandHandler,
    ConversationHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

import internal_requests.service as api_service

from conversations.task_1.keyboards import (
    get_inline_keyboard,
)
from internal_requests.entities import Answer


CHOOSING = 1
CHOICES_SIX_LETTERS = "АБВГДЕ"
CHOICES_TWO_LETTERS = "АБ"
LABEL_PATTERN = r"\[([А-Я])\]"
IDX_IN_STR = 4
MAX_SCORE = 5
SCORES = {
    0: " 0️⃣ Баллов",
    1: " 1️⃣ Балл",
    2: " 2️⃣ Баллa",
    3: " 3️⃣ Баллa",
    4: " 4️⃣ Баллa",
    5: " 5️⃣ Баллов",
}

# Константы, относящиеся к Task 1
TASK_ONE_DESCRIPTION = (
    "Далее будет 10 вопросов, в каждом из них – шесть утверждений.\n"
    "Выбирай утверждения в каждом вопросе по степени привлекательности"
)
TASK_ONE_RESULT_INTRO = "<b>У тебя склонность к:</b>"

# Константы, относящиеся к Task 2
TASK_TWO_DESCRIPTION = (
    "Ниже 70 вопросов, в каждом из них – два утверждения. Выбери то "
    "продолжение, которое свойственно тебе больше всего. Важно: подолгу не "
    "задумывайся над ответами!\n\n"
)

# Константы, относящиеся к Task 3
TASK_THREE_DESCRIPTION = (
    "Сейчас тебе будут представлены 42 пары различных видов деятельности. "
    "Если бы тебе пришлось выбирать лишь одну работу из каждой пары, "
    "что бы ты предпочёл?\n\n"
)
TASK_THREE_RESULT_INTRO = "<b>Твой тип личности:</b>"
TASK_THREE_CANCELLATION_TEXT = (
    "Прохождение задания прервано. Если хочешь начать его сначала,"
    ' то ты можешь открыть меню, перейти в "Мои задания" и выбрать Задание 3.'
)

# Константы, относящиеся ко всем заданиям
START_QUESTION_NUMBER = 1
NEXT_KEYBOARD = InlineKeyboardMarkup(
    ((InlineKeyboardButton(text="Далее", callback_data="Далее"),),)
)

TASK_ONE_DATA = {
    "task_number": 1,
    # нужно будет переписать, чтобы это считывалось из базы данных
    "number_of_questions": 10,
    "entry_point_button_label": "Задание 1",
    "description": TASK_ONE_DESCRIPTION,
    "cancel_text": "Выполнение задания 1 было пропущено",
    "choices": CHOICES_SIX_LETTERS,
    "result_intro": TASK_ONE_RESULT_INTRO
}

TASK_TWO_DATA = {
    "task_number": 2,
    # нужно будет переписать, чтобы это считывалось из базы данных
    "number_of_questions": 70,
    "entry_point_button_label": "Задание 2",
    "description": TASK_TWO_DESCRIPTION,
    "cancel_text": "Выполнение задания 2 было пропущено",
    "choices": CHOICES_TWO_LETTERS,
    "result_intro": ""
}

TASK_THREE_DATA = {
    "task_number": 3,
    # нужно будет переписать, чтобы это считывалось из базы данных
    "number_of_questions": 42,
    "entry_point_button_label": "Задание 3",
    "description": TASK_THREE_DESCRIPTION,
    "cancel_text": TASK_THREE_CANCELLATION_TEXT,
    "choices": CHOICES_TWO_LETTERS,
    "result_intro": TASK_THREE_RESULT_INTRO
}


def get_default_inline_keyboard(
    buttons: str, picked_choices: str = ""
) -> InlineKeyboardMarkup:
    """
    Добавляет кнопки в клавиатуре в зависимости от типа задания.
    """
    keyboard = []
    for label in buttons:
        if label not in picked_choices:
            keyboard.append(InlineKeyboardButton(label, callback_data=label))
    return InlineKeyboardMarkup([keyboard])


@dataclass
class BaseTaskConversation:
    """
    Базовый класс для общего управления диалогами, ответственными за
    прохождение заданий.
    """
    task_number: int
    number_of_questions: int
    entry_point_button_label: str
    description: str
    cancel_text: str
    choices: str
    result_intro: str

    def __post_init__(self):
        self.question_method = self.show_question
        self.update_method = self.handle_user_answer

    async def show_task_description(
        self,
        update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> int:
        """
        Выводит инструкцию по прохождению задания.
        Вызывается из CallbackQueryHandler в методе set_entry_points.
        Возвращает CHOOSING (число, равное 1), чтобы диалог перешел
        в состояние CHOOSING.
        """
        description = self.description
        query = update.callback_query
        if query is not None:
            await query.message.edit_reply_markup()
        context.user_data["current_question"] = START_QUESTION_NUMBER
        await update.effective_message.reply_text(
            text=description,
            reply_markup=NEXT_KEYBOARD,
        )
        return CHOOSING

    async def cancel(
        self,
        update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> int:
        """
        Прерывает выполнение задания и выводит сообщение об этом.
        Вызывается из CallbackQueryHandler в методе set_fallbacks.
        """
        await update.message.reply_text(self.cancel_text)
        context.user_data.clear()
        return ConversationHandler.END

    # В task 2 и task 3 такой метод назывался start_question
    async def show_question(
        self,
        update: Update, _context: ContextTypes.DEFAULT_TYPE, question_number: int = 1
    ) -> None:
        """Начинает новый вопрос."""
        print("Метод show_question начал работу")
        # Добавление этой строки приводит к ошибке при запуске Задания 2:
        # telegram.error.BadRequest: Message is not modified: specified new
        # message content and reply markup are exactly the same as a current
        # content and reply markup of the message
        # await update.callback_query.edit_message_reply_markup()
        # При этом кнопка Далее никуда не девается
        await update.callback_query.answer()
        messages = await api_service.get_messages_with_question(
            task_number=2,
            question_number=question_number,
        )
        await update.effective_message.reply_text(
            text=messages[0].content,
            reply_markup=get_default_inline_keyboard(self.choices),
            parse_mode=ParseMode.HTML,
        )
        await update.callback_query.answer()

# В task 2 и task 3 этот метод назывался update_question
    async def handle_user_answer(
        self,
        update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> int:
        """
        Обрабатывает ответ пользователя на вопрос.
        """
        print("Я внутри метода handle_user_answer")
        picked_choice = update.callback_query.data
        message = update.effective_message
        print(f"picked_choice — {picked_choice}")
        print(f"message — {message}")
        await message.edit_text(
            text=f"{message.text_html}\n\nОтвет: {picked_choice.upper()}",
            parse_mode=ParseMode.HTML,
        )
        current_question = context.user_data.get("current_question")
        print(f"current_question: {current_question}")
        print(f"task_number = {self.task_number}")
        await api_service.create_answer(
            Answer(
                telegram_id=message.chat_id,
                task_number=self.task_number,
                number=current_question,
                content=update.callback_query.data,
            )
        )
        print("api_service worked successfully")
        if current_question == self.number_of_questions:
            print('Это был последний вопрос')
            state = await self.show_result(update, context)
            return state
        context.user_data["current_question"] += 1
        print("context.user_data:")
        print(context.user_data)
        await self.show_question(
            update, context, context.user_data.get("current_question"))
        return CHOOSING

    async def show_result(
        self,
        update: Update, context: ContextTypes.DEFAULT_TYPE
    ):
        """
        Выводит результаты пользователя и завершает диалог текущего задания,
        после чего переходит к следующему.
        """
        query = update.callback_query
        if self.result_intro:
            await query.message.reply_text(
                text=self.result_intro,
                parse_mode=ParseMode.HTML,
            )
        results = await api_service.get_messages_with_results(
            telegram_id=query.from_user.id, task_number=self.task_number
        )
        for result in results[:-1]:
            await query.message.reply_text(
                text=result.content,
                parse_mode=ParseMode.HTML,
            )
        await query.message.reply_text(
            text=results[-1].content,
            parse_mode=ParseMode.HTML,
            reply_markup=InlineKeyboardMarkup(
                ((InlineKeyboardButton(text=f"Задание {self.task_number + 1}",
                 callback_data=f"start_task_{self.task_number + 1}"),),)
            ),
        )
        context.user_data.clear()
        return ConversationHandler.END

    def set_entry_points(self):
        """
        Описывает entry_points для вхождения в диалог.
        Нужно использовать при создании хэндлера для задания.
        """
        return [
            MessageHandler(
                filters.Regex(self.entry_point_button_label),
                self.show_task_description
            ),
            CallbackQueryHandler(
                self.show_task_description,
                pattern=rf"^start_task_{self.task_number}$"
            )
        ]

    def set_states(self):
        """
        Управляет ведением диалога.
        Нужно использовать при создании хэндлера для задания.
        """
        return {
            CHOOSING: [
                CallbackQueryHandler(self.question_method, pattern=r"^Далее$"),
                CallbackQueryHandler(
                    self.update_method, pattern=f"^([{self.choices}])$")
            ]
        }

    def set_fallbacks(self):
        """
        Управляет выходом из диалога.
        Нужно использовать при создании хэндлера для задания.
        """
        return [CommandHandler("cancel", self.cancel)]

    def add_handlers(self):
        """
        Добавляет хэндлеры для обработки задания: entry_points, states и fallbacks.
        """
        return ConversationHandler(
            entry_points=self.set_entry_points(),
            states=self.set_states(),
            fallbacks=self.set_fallbacks(),
        )


class TaskOneConversation(BaseTaskConversation):
    """
    Класс для обработки диалогов в Задании 1. В классе переопределяется метод
    отображения вопросов и метод обработки ответов пользователя.
    """
    async def show_question(
        self,
        update: Update, context: ContextTypes.DEFAULT_TYPE, question_number: int = 1
    ) -> None:
        """
        Выводит вопросы в Задании 1: текст вопроса + клавиатура
        АБВГДЕ с вариантами ответов.
        """
        # Эта строка печатается, когда нажимаешь кнопку Далее, прочитав описание задания
        print("Метод get_start_question начал работу")
        await update.callback_query.answer()
        context.user_data["picked_choices"] = ""
        # Вытаскивает из базы данных первый вопрос
        messages = await api_service.get_messages_with_question(
            task_number=1,
            question_number=question_number,
        )
        await update.effective_message.reply_text(
            text=messages[0].content,
            reply_markup=get_inline_keyboard(self.choices),
            parse_mode=ParseMode.HTML,
        )

    def _get_question_text(
        self, message_text, picked_choices: str = ""
    ) -> str:
        text = f"{message_text[0]}\n\n"
        for string in message_text[1:]:
            text += f"{string}"
            if re.search(LABEL_PATTERN, string).group(1) == picked_choices[-1]:
                text += (
                    f" — {SCORES[MAX_SCORE - picked_choices.index(string[IDX_IN_STR])]}"
                )
            text += "\n\n"
        return text

    async def _save_answer(
        self, user_id, current_question, picked_choices
    ):
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

    async def handle_user_answer(
        self,
        update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> int:
        """
        Обрабатывает ответ пользователя на вопрос: при нажатии на вариант
        ответа, записывает этот вариант и убирает его из списка вариантов на
        клавиатуре.
        """
        print("Я внутри метода handle_user_answer")
        choice = update.callback_query.data
        context.user_data["picked_choices"] += choice
        picked_choices = context.user_data.get("picked_choices")
        message = update.effective_message
        await update.effective_message.edit_text(
            self._get_question_text(message.text_html.split("\n\n"), picked_choices),
            reply_markup=get_inline_keyboard(self.choices, picked_choices),
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


task_one = TaskOneConversation(**TASK_ONE_DATA)
task_two = BaseTaskConversation(**TASK_TWO_DATA)
task_three = BaseTaskConversation(**TASK_THREE_DATA)

task_one_handler = task_one.add_handlers()
task_two_handler = task_two.add_handlers()
task_three_handler = task_three.add_handlers()
