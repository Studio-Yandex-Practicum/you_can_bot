import logging

from telegram import ForceReply, InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    CallbackQueryHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

from conversations.tasks.base import (
    CHOOSING,
    CONFIRM_BUTTON_PATTERN,
    CONFIRMING,
    NEXT_BUTTON_PATTERN,
    SEND_ANSWER_TEXT,
    TYPING_ANSWER,
    BaseTaskConversation,
)
from conversations.tasks.keyboards import CONFIRM_KEYBOARD
from internal_requests import service as api_service
from internal_requests.entities import Answer
from utils.error_handler import error_decorator

_LOGGER = logging.getLogger(__name__)


class TaskSixConversation(BaseTaskConversation):
    """
    Класс для обработки диалогов в Задании 6.
    Хэндлер для обработки ответов пользователя заменен на MessageHandler,
    пользователь отправляет ответы в виде текстовых сообщений.
    """

    @error_decorator(logger=_LOGGER)
    async def show_question(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> int:
        """
        Показывает очередной вопрос, относящийся к текущему заданию.
        """
        current_question = context.user_data["current_question"]
        if current_question == 1:
            await update.callback_query.answer()
            await update.callback_query.edit_message_reply_markup()
        messages = await api_service.get_messages_with_question(
            task_number=self.task_number,
            question_number=current_question,
        )
        await update.effective_message.reply_text(
            text=messages[0].content,
            reply_markup=ForceReply(selective=True),
        )
        await update.callback_query.answer()
        return TYPING_ANSWER

    async def show_result(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Выводит результаты пользователя и завершает диалог текущего задания,
        после чего переходит к следующему заданию.
        """
        await update.effective_message.reply_text(
            text=self.result_intro,
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

    @error_decorator(logger=_LOGGER)
    async def handle_typed_answer(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> int:
        """
        Принимает текстовый ответ пользователя на текущий вопрос и запрашивает у
        пользователя подтверждение на сохранение текущего варианта ответа.
        """
        answer_text = update.message.text
        answer_id = update.message.message_id
        confirmation_message = await update.effective_message.reply_text(
            text=SEND_ANSWER_TEXT + '"' + answer_text + '"',
            reply_markup=CONFIRM_KEYBOARD,
        )
        context.user_data["confirmation_message_id"] = confirmation_message.message_id

        if answer_text and answer_id:
            context.user_data["answer_text"] = answer_text
            context.user_data["answer_id"] = answer_id
        return CONFIRMING

    @error_decorator(logger=_LOGGER)
    async def handle_answer_editing(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> int:
        """
        Обрабатывает редактирование ответа пользователя. Если пользователь редактирует
        сообщение с ответом на текущий вопрос, то сохраняет новый текст ответа и
        запрашивает подтверждение.
        """
        original_answer_id = context.user_data.get("answer_id")
        if update.edited_message.message_id == original_answer_id:
            answer_text = update.edited_message.text
            answer_id = update.edited_message.message_id
            confirmation_message_id = context.user_data.get("confirmation_message_id")
            if confirmation_message_id:
                await context.bot.edit_message_text(
                    chat_id=update.effective_chat.id,
                    message_id=confirmation_message_id,
                    text=SEND_ANSWER_TEXT + '"' + answer_text + '"',
                    reply_markup=CONFIRM_KEYBOARD,
                )

            if answer_text and answer_id:
                context.user_data["answer_text"] = answer_text
                context.user_data["answer_id"] = answer_id
        return CONFIRMING

    @error_decorator(logger=_LOGGER)
    async def save_answer(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> int:
        """
        Если до этого этапа пользователю отправлялось сообщение с запросом на
        подтверждение ответа, то удаляет это сообщение. Сохраняет ответ пользователя
        на текущий вопрос. Переводит диалог к демонстрации следующего вопроса или к
        оповещению о завершении задания, если вопросы закончились.
        """
        confirmation_message_id = context.user_data.get("confirmation_message_id")
        if confirmation_message_id:
            await context.bot.delete_message(
                chat_id=update.effective_chat.id,
                message_id=confirmation_message_id,
            )
        answer_text = context.user_data.get("answer_text")
        current_question_number = context.user_data.get("current_question")
        await api_service.create_answer(
            answer=Answer(
                telegram_id=update.effective_message.chat_id,
                task_number=self.task_number,
                number=current_question_number,
                content=answer_text,
            )
        )

        if current_question_number == self.number_of_questions:
            return await self.show_result(update, context)
        context.user_data["current_question"] += 1
        await self.show_question(update, context)
        return TYPING_ANSWER

    def set_states(self):
        """
        Управляет ведением диалога.
        Используется при создании хэндлера для задания.
        """
        return {
            CHOOSING: [
                CallbackQueryHandler(
                    callback=self.question_method, pattern=NEXT_BUTTON_PATTERN
                )
            ],
            TYPING_ANSWER: [
                MessageHandler(
                    filters=filters.TEXT & ~filters.COMMAND,
                    callback=self.handle_typed_answer,
                )
            ],
            CONFIRMING: [
                CallbackQueryHandler(
                    callback=self.save_answer, pattern=CONFIRM_BUTTON_PATTERN
                ),
                MessageHandler(
                    filters=filters.UpdateType.EDITED_MESSAGE,
                    callback=self.handle_answer_editing,
                ),
            ],
        }
