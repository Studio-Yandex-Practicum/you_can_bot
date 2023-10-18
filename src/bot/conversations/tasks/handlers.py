from telegram.ext import (
    CallbackQueryHandler,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    filters,
)

from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes, ConversationHandler, CallbackContext
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from conversations.task_1.callback_funcs import (
    CHOICES,
    CHOOSING,
    get_answer_question,
)

from conversations.task_2.callback_funcs import (
    update_question
)

import internal_requests.service as api_service
from conversations.task_1.keyboards import (
    GO_TO_TASK_2_KEYBOARD,
    START_TASK_1_KEYBOARD,
    get_inline_keyboard,
)
from internal_requests.entities import Answer

REPLY_KEYBOARD = InlineKeyboardMarkup.from_row(
    (
        InlineKeyboardButton(text="А", callback_data="А"),
        InlineKeyboardButton(text="Б", callback_data="Б"),
    ),
)

def get_default_inline_keyboard(buttons: str, picked_choices: str = "") -> InlineKeyboardMarkup:
    """Добавляет кнопки в сообщении с учетом уже выбранных ответов."""
    keyboard = []
    for label in buttons:
        if label not in picked_choices:
            keyboard.append(InlineKeyboardButton(label, callback_data=label))
    return InlineKeyboardMarkup([keyboard])


CHOICES_TYPE_ONE = "АБВГДЕ"
CHOICES_TYPE_TWO = "АБ"

TASK_ONE_DESCRIPTION = (
    "Далее будет 10 вопросов, в каждом из них – шесть утверждений.\n"
    "Выбирай утверждения в каждом вопросе по степени привлекательности"
)
TASK_TWO_DESCRIPTION = (
    "Ниже 70 вопросов, в каждом из них – два утверждения. Выбери то "
    "продолжение, которое свойственно тебе больше всего. Важно: подолгу не "
    "задумывайся над ответами!\n\n"
)
START_QUESTION_NUMBER = 1
NEXT_KEYBOARD = InlineKeyboardMarkup(
    ((InlineKeyboardButton(text="Далее", callback_data="Далее"),),)
)

TASK_ONE_DATA = {
    "task_number": 1,
    # нужно будет переписать, чтобы это считывалось из базы данных
    "number_of_questions": 10,
    "task_name": "Задание 1",
    "description": TASK_ONE_DESCRIPTION,
    "cancel_text": "Выполнение задания 1 было пропущено",
    "choices": CHOICES_TYPE_ONE,
}

TASK_TWO_DATA = {
    "task_number": 2,
    # нужно будет переписать, чтобы это считывалось из базы данных
    "number_of_questions": 70,
    "task_name": "Задание 2",
    "description": TASK_TWO_DESCRIPTION,
    "cancel_text": "Выполнение задания 2 было пропущено",
    "choices": CHOICES_TYPE_TWO,
}


class BaseTaskConversation:
    """
    Класс для общего управления диалогами, ответственными за прохождение
    заданий.
    """
    def __init__(
        self,
        task_data,
        # question_method,
        # update_method
    ):
        self.task_number = task_data["task_number"]
        self.number_of_questions = task_data["number_of_questions"]
        self.entry_point_button_label = task_data["task_name"]
        self.description = task_data["description"]
        self.cancel_text = task_data["cancel_text"]
        # self.question_method = question_method
        # if task_data["task_number"] == 1:
        if self.task_number == 1:
            self.question_method = self.get_start_question_type_one
            self.update_method = get_answer_question
        else:
            self.question_method = self.show_question
            self.question_method = self.question_method
        # self.update_method = update_method

        self.update_method = self.handle_user_answer
        self.choices = task_data["choices"]

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

    async def get_start_question_type_one(
        self,
        update: Update, context: ContextTypes.DEFAULT_TYPE, question_number: int = 1
    ) -> None:
        """
        Выводит первый вопрос задания.
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

    # В task 2 и task 3 такой метод назывался start_question
    async def show_question(
        self,
        update: Update, _context: ContextTypes.DEFAULT_TYPE, question_number: int = 1
    ) -> None:
        """Начинает новый вопрос."""
        print("Метод show_question начал работу")
        await update.callback_query.answer()
        messages = await api_service.get_messages_with_question(
            task_number=2,
            question_number=question_number,
        )
        # reply_markup = REPLY_KEYBOARD
        await update.effective_message.reply_text(
            text=messages[0].content,
            # reply_markup=REPLY_KEYBOARD,
            # reply_markup=get_inline_keyboard(self.choices),
            reply_markup=get_default_inline_keyboard(self.choices),
            parse_mode=ParseMode.HTML,
        )
        await update.callback_query.answer()

# В task 2 и task 3 этот метод назывался update_question
    async def handle_user_answer(
        self,
        update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """
        Обрабатывает ответ пользователя на вопрос.
        """
        print("Я внутри метода handle_user_answer")
        picked_choice = update.callback_query.data
        message = update.effective_message
        # Здесь к тексту сообщения и вариантам ответов аппендится ответ пользователя
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
            context.user_data.clear()
            print('Это был последний вопрос')
            return await self.show_result(update, context)
        context.user_data["current_question"] += 1
        print("context.user_data:")
        print(context.user_data)
        await self.show_question(update, context, context.user_data.get("current_question"))
        return CHOOSING

    async def show_result(
        self,
        update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Расшифровка."""
        query = update.callback_query
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
            reply_markup=REPLY_KEYBOARD, # поменять на клавиатуру, переходящую к следующему заданию
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
                pattern=r"^show_task_description$",
            ),
        ]

    def set_states(self):
        """
        Управляет ведением диалога.
        Нужно использовать при создании хэндлера для задания.
        """
        return {
            CHOOSING: [
                CallbackQueryHandler(self.question_method, pattern=r"^Далее$"),
                CallbackQueryHandler(self.update_method, pattern=f"^([{self.choices}])$")
                # CallbackQueryHandler(self.update_method, pattern=f"^([{CHOICES}])$")
            ]
        }

    def set_fallbacks(self):
        """
        Управляет выходом из диалога.
        Нужно использовать при создании хэндлера для задания.
        """
        return [CommandHandler("cancel", self.cancel)]


task_one = BaseTaskConversation(
    TASK_ONE_DATA,
    # get_start_question,
    # get_answer_question,
)

task_two = BaseTaskConversation(
    TASK_TWO_DATA,
    # start_question,
    # update_question,
)

task_one_handler = ConversationHandler(
    entry_points=task_one.set_entry_points(),
    states=task_one.set_states(),
    fallbacks=task_one.set_fallbacks(),
)

task_two_handler = ConversationHandler(
    entry_points=task_two.set_entry_points(),
    states=task_two.set_states(),
    fallbacks=task_two.set_fallbacks(),
)


#BACKUPS

# async def start_task_1(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
#     """Выводит описание задания 1."""
#     query = update.callback_query
#     print(query)
#     if query is not None:
#         await query.message.edit_reply_markup()
#     context.user_data["current_question"] = START_QUESTION_NUMBER
#     await update.effective_message.reply_text(
#         text=START_TASK_1_TEXT,
#         reply_markup=NEXT_KEYBOARD,
#     )
#     return CHOOSING

# async def show_start_of_task_2(
#     update: Update, context: ContextTypes.DEFAULT_TYPE
# ) -> int:
#     """Вывод описания задания 2."""
#     query = update.callback_query
#     if query is not None:
#         await query.message.edit_reply_markup()
#     context.user_data["current_question"] = START_QUESTION_NUMBER
#     await update.effective_message.reply_text(
#         text=TEXT_OF_START_OF_TASK_2,
#         reply_markup=NEXT_KEYBOARD,
#     )
#     return CHOOSING

# Эта штука дает возможность обращаться с текстом от юзера
# user_message = update.message # Выдает длинную колбасу с данными
# update.message.text # Выводит только текст сообщения, введенного пользователем


# GREETING_BUTTON_LABEL = 'Привет'

# GREETING_KEYBOARD = InlineKeyboardMarkup(
#     inline_keyboard=[
#         [InlineKeyboardButton(GREETING_BUTTON_LABEL, callback_data="greeting")]
#     ],
# )


# class TaskOneConversation(BaseTaskConversation):
#     def __init__(self):
#         print("Inside TaskOneConversation")
#         super().__init__(
#             TASK_BUTTON_LABELS.get('FIRST'),
#             start_task_1,
#             get_start_question,
#             get_answer_question
#         )

# task_one = TaskOneConversation()

# task_one = BaseTaskConversation(
#     TASK_BUTTON_LABELS.get('ONE'),
#     start_task_1,
#     get_start_question,
#     get_answer_question,
# )

# task_handler = ConversationHandler(
#     entry_points=[
#         MessageHandler(filters.Regex(TASK_BUTTON_LABELS.get('FIRST')), start_task_1),
#         CallbackQueryHandler(start_task_1, r"^start_task_1$"),
#     ],
#     states={
#         CHOOSING: [
#             CallbackQueryHandler(get_start_question, pattern=r"^Далее$"),
#             CallbackQueryHandler(get_answer_question, pattern=f"^([{CHOICES}])$"),
#         ],
#     },
#     fallbacks=[CommandHandler("cancel", cancel)],
# )

# task_2_handler: ConversationHandler = ConversationHandler(
#     entry_points=[
#         MessageHandler(
#             filters.Regex(TEXT_ENTRY_POINT_BUTTON_FOR_TASK_2), show_start_of_task_2
#         ),
#         CallbackQueryHandler(show_start_of_task_2, r"^start_task_2$"),
#     ],
#     states={
#         CHOOSING: [
#             CallbackQueryHandler(start_question, pattern=r"^Далее$"),
#             CallbackQueryHandler(update_question, pattern=r"^(а|б)$"),
#         ]
#     },
#     fallbacks=[CommandHandler(CANCEL_COMMAND, cancel)],
# )

# task_3_handler: ConversationHandler = ConversationHandler(
#     entry_points=[
#         MessageHandler(
#             filters.Regex(TEXT_ENTRY_POINT_BUTTON_FOR_TASK_3), show_start_of_task_3
#         ),
#         CallbackQueryHandler(show_start_of_task_3, r"^start_task_3$"),
#     ],
#     states={
#         CHOOSING: [
#             CallbackQueryHandler(start_question, pattern=r"^Далее$"),
#             CallbackQueryHandler(update_question, pattern=r"^(а|б)$"),
#         ]
#     },
#     fallbacks=[CommandHandler(CANCEL_COMMAND, cancel)],
# )


# async def show_task_description(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     query = update.callback_query
#     print("I'm task description and I work")
    # print(context.chat_data)
    # print(context.user_data)
    # распечатывает объект update:
    # print(update)
    # распечатывает объект context в удобочитаемом виде:
    # for attr in dir(context):
    #     print(f"{attr}: {getattr(context, attr)}")

# task_handler = ConversationHandler(
#     entry_points=[
#         # MessageHandler(filters.Regex('penguin'), show_task_description), # работает
#         MessageHandler(filters.Regex('penguin'), show_task_description),
#         CallbackQueryHandler(show_task_description, r"^greeting$"),
#         # CallbackQueryHandler(show_task_description, r"^penguin$"),
#     ],
#     states={
#         CHOOSING: [
#             CallbackQueryHandler(get_start_question, pattern=r"^Далее$"),
#             CallbackQueryHandler(get_answer_question, pattern=f"^([{CHOICES}])$"),
#         ],
#     },
#     fallbacks=[CommandHandler("cancel", cancel)],
# )



# task_handler = ConversationHandler(
#     entry_points=[
#         MessageHandler(filters.Regex(TASK_BUTTON_LABELS.get('FIRST')), start_task_1),
#         CallbackQueryHandler(start_task_1, r"^start_task_1$"),
#     ],
#     states={
#         CHOOSING: [
#             CallbackQueryHandler(get_start_question, pattern=r"^Далее$"),
#             CallbackQueryHandler(get_answer_question, pattern=f"^([{CHOICES}])$"),
#         ],
#     },
#     fallbacks=[CommandHandler("cancel", cancel)],
# )


# async def start_task_1(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
#     """Выводит описание задания 1."""
#     query = update.callback_query
#     if query is not None:
#         await query.message.edit_reply_markup()
#     context.user_data["current_question"] = START_QUESTION_NUMBER
#     await update.effective_message.reply_text(
#         text=START_TASK_1_TEXT,
#         reply_markup=START_TASK_1_KEYBOARD,
#     )
#     return CHOOSING