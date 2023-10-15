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
    # cancel,
    get_answer_question,
    get_start_question,
)

from conversations.task_2.callback_funcs import (
    start_question
)

import internal_requests.service as api_service
from conversations.task_1.keyboards import (
    GO_TO_TASK_2_KEYBOARD,
    START_TASK_1_KEYBOARD,
    get_inline_keyboard,
)

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
    "task_name": "Задание 1",
    "description": TASK_ONE_DESCRIPTION,
    "cancel_text": "Выполнение задания 1 было пропущено",
}

TASK_TWO_DATA = {
    "task_name": "Задание 2",
    "description": TASK_TWO_DESCRIPTION,
    "cancel_text": "Выполнение задания 2 было пропущено",
}


class BaseTaskConversation:
    """
    Класс для общего управления диалогами, ответственными за прохождение
    заданий.
    """
    def __init__(
        self,
        task_data,
        question_method,
        update_method
    ):
        self.entry_point_button_label = task_data["task_name"]
        self.description = task_data["description"]
        self.cancel_text = task_data["cancel_text"]
        self.question_method = question_method
        self.question_method = self.question_method
        self.update_method = update_method

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

    # async def get_start_question(
    #     self,
    #     update: Update, context: ContextTypes.DEFAULT_TYPE, question_number: int = 1
    # ) -> None:
    #     """Начинает новый вопрос."""
    #     await update.callback_query.answer()
    #     context.user_data["picked_choices"] = ""
    #     messages = await api_service.get_messages_with_question(
    #         task_number=1,
    #         question_number=question_number,
    #     )
    #     await update.effective_message.reply_text(
    #         text=messages[0].content,
    #         reply_markup=get_inline_keyboard(CHOICES),
    #         parse_mode=ParseMode.HTML,
    #     )

    # async def start_question(
    #     update: Update, _context: ContextTypes.DEFAULT_TYPE, question_number: int = 1
    # ) -> None:
    #     """Начинает новый вопрос."""
    #     await update.callback_query.answer()
    #     messages = await api_service.get_messages_with_question(
    #         task_number=CURRENT_TASK,
    #         question_number=question_number,
    #     )
    #     await update.effective_message.reply_text(
    #         text=messages[0].content,
    #         reply_markup=REPLY_KEYBOARD,
    #         parse_mode=ParseMode.HTML,
    #     )


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
                CallbackQueryHandler(self.update_method, pattern=f"^([{CHOICES}])$")
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
    get_start_question,
    get_answer_question,
)

task_two = BaseTaskConversation(
    TASK_TWO_DATA,
    # get_start_question,
    start_question,
    get_answer_question,
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