from dataclasses import dataclass

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.constants import ParseMode
from telegram.ext import (
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

from conversations.tasks.keyboards import NEXT_KEYBOARD, get_default_inline_keyboard
from internal_requests import service as api_service
from internal_requests.entities import Answer

CHOOSING = 1
START_QUESTION_NUMBER = 1
BUTTON_LABELS_PATTERN = r"^([1-9]|10|[А-Е])$"
NEXT_BUTTON_PATTERN = r"^Далее$"
TASK_CANCEL_TEXT = (
    "Прохождение задания прервано. Если захочешь продолжить его"
    ' выполнение, то можешь открыть меню, перейти в "Посмотреть'
    ' все задания" или ввести команду /tasks и выбрать'
    " Задание "
)
TASK_START_BUTTON_LABEL = "Задание "


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
        self.entry_point_button_label: str = TASK_START_BUTTON_LABEL + str(
            self.task_number
        )
        self.cancel_text: str = TASK_CANCEL_TEXT + str(self.task_number) + "."
        self.question_method = self.show_question
        self.update_method = self.handle_user_answer

    async def show_task_description(
            self, update: Update, context: ContextTypes.DEFAULT_TYPE
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

    async def show_question(
            self,
            update: Update,
            _context: ContextTypes.DEFAULT_TYPE,
            question_number: int = 1,
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
            self, update: Update, context: ContextTypes.DEFAULT_TYPE
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
                content=update.callback_query.data.lower(),
            )
        )
        if current_question == self.number_of_questions:
            state = await self.show_result(update, context)
            return state
        context.user_data["current_question"] += 1
        await self.show_question(
            update, context, context.user_data.get("current_question")
        )
        return CHOOSING

    async def show_result(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
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
                (
                    (
                        InlineKeyboardButton(
                            text=f"Задание {self.task_number + 1}",
                            callback_data=f"start_task_{self.task_number + 1}",
                        ),
                    ),
                )
            ),
        )
        context.user_data.clear()
        return ConversationHandler.END

    async def cancel(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """
        Прерывает выполнение задания и выводит сообщение об этом.
        Вызывается из CallbackQueryHandler в методе set_fallbacks.
        """
        await update.message.reply_text(self.cancel_text)
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
                self.show_task_description_with_number
            ),
            CallbackQueryHandler(
                self.show_task_description_with_number,
                pattern=rf"^start_task:{self.task_number}:with_choice$"
            ),
        ]

    def set_states(self):
        """
        Управляет ведением диалога.
        Используется при создании хэндлера для задания.
        """
        return {
            CHOOSING: [
                CallbackQueryHandler(self.question_method, pattern=NEXT_BUTTON_PATTERN),
                CallbackQueryHandler(self.update_method, pattern=BUTTON_LABELS_PATTERN),
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

    async def show_task_description_with_number(
            self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> int:
        """Показывает описание задание, но перед
        этим добавляет в предыдущее сообщение выбранный номер задания."""
        query = update.callback_query
        if query is not None:
            await query.message.edit_reply_markup()
        task_number = self.task_number
        description = f"Выбранное задание: {task_number}\n\n{self.description}"
        context.user_data["current_question"] = START_QUESTION_NUMBER
        await update.effective_message.reply_text(
            text=description,
            reply_markup=NEXT_KEYBOARD,
        )
        return CHOOSING
