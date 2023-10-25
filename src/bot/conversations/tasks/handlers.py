import re

from dataclasses import dataclass
# from typing import Tuple

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

from internal_requests.entities import Answer

from .keyboards import get_default_inline_keyboard

CHOOSING = 1
LABEL_PATTERN = r"\[([А-Я])\]"
IDX_IN_STR = 4
MAX_SCORE = 5
START_QUESTION_NUMBER = 1

# Константы, относящиеся к клавиатурам
BUTTON_LABELS_PATTERN = r"^([1-9]|10|[А-Е])$"
NEXT_BUTTON_PATTERN = r"^Далее$"
# MAX_BUTTON_NUMBER = 5
# MAX_TELEGRAM_ROW_LENGTH = 8
NEXT_KEYBOARD = InlineKeyboardMarkup(
    ((InlineKeyboardButton(text="Далее", callback_data="Далее"),),)
)
CHOICES_SIX_LETTERS = ("А", "Б", "В", "Г", "Д", "Е")
CHOICES_TWO_LETTERS = ("А", "Б")
CHOICES_TEN_NUMBERS = ("1", "2", "3", "4", "5", "6", "7", "8", "9", "10")
SCORES = {
    0: " 0️⃣ Баллов",
    1: " 1️⃣ Балл",
    2: " 2️⃣ Баллa",
    3: " 3️⃣ Баллa",
    4: " 4️⃣ Баллa",
    5: " 5️⃣ Баллов",
}

# номер задания добавляется при создании экземпляра класса
TASK_CANCEL_TEXT = (
    "Прохождение задания прервано. Если захочешь продолжить его"
    ' выполнение, то можешь открыть меню, перейти в "Посмотреть'
    ' все задания" или ввести команду /tasks и выбрать'
    ' Задание '
)
# номер задания добавляется при создании экземпляра класса
TASK_START_BUTTON_LABEL = "Задание "

# Константы, относящиеся к Task 1
TASK_ONE_NUMBER = 1
TASK_ONE_NUM_OF_QUESTIONS = 10
TASK_ONE_DESCRIPTION = (
    "Далее будет 10 вопросов, в каждом из них – шесть утверждений.\n"
    "Выбирай утверждения в каждом вопросе по степени привлекательности"
)
TASK_ONE_RESULT_INTRO = "<b>У тебя склонность к:</b>"

# Константы, относящиеся к Task 2
TASK_TWO_NUMBER = 2
TASK_TWO_NUM_OF_QUESTIONS = 70
TASK_TWO_DESCRIPTION = (
    "Ниже 70 вопросов, в каждом из них – два утверждения. Выбери то "
    "продолжение, которое свойственно тебе больше всего. Важно: подолгу не "
    "задумывайся над ответами!\n\n"
)

# Константы, относящиеся к Task 3
TASK_THREE_NUMBER = 3
TASK_THREE_NUM_OF_QUESTIONS = 42
TASK_THREE_DESCRIPTION = (
    "Сейчас тебе будут представлены 42 пары различных видов деятельности. "
    "Если бы тебе пришлось выбирать лишь одну работу из каждой пары, "
    "что бы ты предпочёл?\n\n"
)
TASK_THREE_RESULT_INTRO = "<b>Твой тип личности:</b>"

# Константы, относящиеся к Task 4
TASK_FOUR_NUMBER = 4
TASK_FOUR_NUM_OF_QUESTIONS = 41
TASK_FOUR_DESCRIPTION = (
    "Насколько ты согласен с каждым из следующих утверждений? "
    "Варианты ответов:\n"
    "1 – совершенно не согласен\n"
    "10 – полностью согласен\n\n"
)
TASK_FOUR_RESULT_INTRO = "Твои ценностные ориентации: \n\n"

TASK_ONE_DATA = {
    "task_number": TASK_ONE_NUMBER,
    "number_of_questions": TASK_ONE_NUM_OF_QUESTIONS,
    "description": TASK_ONE_DESCRIPTION,
    "choices": CHOICES_SIX_LETTERS,
    "result_intro": TASK_ONE_RESULT_INTRO
}

TASK_TWO_DATA = {
    "task_number": TASK_TWO_NUMBER,
    "number_of_questions": TASK_TWO_NUM_OF_QUESTIONS,
    "description": TASK_TWO_DESCRIPTION,
    "choices": CHOICES_TWO_LETTERS,
    "result_intro": ""
}

TASK_THREE_DATA = {
    "task_number": TASK_THREE_NUMBER,
    "number_of_questions": TASK_THREE_NUM_OF_QUESTIONS,
    "description": TASK_THREE_DESCRIPTION,
    "choices": CHOICES_TWO_LETTERS,
    "result_intro": TASK_THREE_RESULT_INTRO
}

TASK_FOUR_DATA = {
    "task_number": TASK_FOUR_NUMBER,
    "number_of_questions": TASK_FOUR_NUM_OF_QUESTIONS,
    "description": TASK_FOUR_DESCRIPTION,
    "choices": CHOICES_TEN_NUMBERS,
    "result_intro": TASK_FOUR_RESULT_INTRO
}


# def get_default_inline_keyboard(
#     button_labels: Tuple[str],
#     picked_choices: str = ""
# ) -> InlineKeyboardMarkup:
#     """
#     Формирует клавиатуру, принимая на вход кортеж кнопок. При формировании
#     учитывает уже выбранные пользователем ответы, исключая такие кнопки
#     из клавиатуры (за исключение ответственен аргумент picked_choices, по
#     умолчанию он является пустой строкой, не влияющей на формирование).
#     По ограничению Telegram, количество кнопок в одном ряду клавиатуры
#     не должно превышать 8, поэтому прописано ограничение MAX_BUTTON_NUMBER.
#     Если количество кнопок превышает 8, то кнопки ставятся в ряды,
#     содержащие MAX_BUTTON_NUMBER. Выходящие за ограничение кнопки
#     переносятся на следующий ряд.
#     """
#     keyboard = []
#     row = []
#     for label in button_labels:
#         if label not in picked_choices:
#             button = InlineKeyboardButton(label, callback_data=label)
#             row.append(button)
#         if (
#             len(row) == MAX_BUTTON_NUMBER
#             and len(button_labels) > MAX_TELEGRAM_ROW_LENGTH
#         ):
#             keyboard.append(row)
#             row = []
#     if row:
#         keyboard.append(row)
#     return InlineKeyboardMarkup(keyboard)


@dataclass
class BaseTaskConversation:
    """
    Базовый класс для общего управления диалогами, ответственными за
    прохождение заданий.
    """
    task_number: int
    number_of_questions: int
    description: str
    choices: str
    result_intro: str

    def __post_init__(self):
        """
        Формирует entry_point для задания, составляя его из номера задания и
        шаблонного текста TASK_START_BUTTON_LABEL.
        Формирует cancel_text для задания, составляя его из номера задания и
        шаблонного текста TASK_CANCEL_TEXT.
        Добавляет методы для отображения вопросов и обработки ответов.
        """
        self.entry_point_button_label: str = (
            TASK_START_BUTTON_LABEL + str(self.task_number)
        )
        self.cancel_text: str = (
            TASK_CANCEL_TEXT + str(self.task_number) + "."
        )
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

    async def show_question(
        self,
        update: Update,
        _context: ContextTypes.DEFAULT_TYPE,
        question_number: int = 1
    ) -> None:
        """
        Показывает очередной вопрос, относящийся к текущему заданию.
        Формирует клавиатуру для ответа на вопрос.
        """
        if question_number == 1:
            await update.callback_query.edit_message_reply_markup()
        messages = await api_service.get_messages_with_question(
            task_number=self.task_number,
            question_number=question_number,
        )
        await update.effective_message.reply_text(
            text=messages[0].content,
            reply_markup=get_default_inline_keyboard(self.choices),
            parse_mode=ParseMode.HTML,
        )
        await update.callback_query.answer()

    async def handle_user_answer(
        self,
        update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> int:
        """
        Обрабатывает ответ пользователя на вопрос и вызывает метод show_question,
        чтобы перейти к следующему вопросу. Если вопрос был последний,
        вызывает show_result, чтобы вывести результат пользователя
        и завершить диалог.
        """
        picked_choice = update.callback_query.data
        message = update.effective_message
        await message.edit_text(
            text=f"{message.text_html}\n\nОтвет: {picked_choice.upper()}",
            parse_mode=ParseMode.HTML,
        )
        current_question = context.user_data.get("current_question")
        await api_service.create_answer(
            Answer(
                telegram_id=message.chat_id,
                task_number=self.task_number,
                number=current_question,
                content=update.callback_query.data,
            )
        )
        if current_question == self.number_of_questions:
            state = await self.show_result(update, context)
            return state
        context.user_data["current_question"] += 1
        await self.show_question(
            update, context, context.user_data.get("current_question"))
        return CHOOSING

    async def show_result(
        self,
        update: Update, context: ContextTypes.DEFAULT_TYPE
    ):
        """
        Выводит результаты пользователя и завершает диалог текущего задания,
        после чего переходит к следующему заданию.
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
        Используется при создании хэндлера для задания.
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
        Используется при создании хэндлера для задания.
        """
        return {
            CHOOSING: [
                CallbackQueryHandler(
                    self.question_method, pattern=NEXT_BUTTON_PATTERN),
                CallbackQueryHandler(
                    self.update_method, pattern=BUTTON_LABELS_PATTERN)
            ]
        }

    def set_fallbacks(self):
        """
        Управляет выходом из диалога.
        Используется при создании хэндлера для задания.
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
        Выводит вопросы в Задании 1: текст вопроса + клавиатура с исходными
        вариантами ответов: А Б В Г Д Е.
        """
        await update.callback_query.answer()
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


task_one = TaskOneConversation(**TASK_ONE_DATA)
task_two = BaseTaskConversation(**TASK_TWO_DATA)
task_three = BaseTaskConversation(**TASK_THREE_DATA)
task_four = BaseTaskConversation(**TASK_FOUR_DATA)

task_one_handler = task_one.add_handlers()
task_two_handler = task_two.add_handlers()
task_three_handler = task_three.add_handlers()
task_four_handler = task_four.add_handlers()
