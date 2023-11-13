from telegram import ForceReply, InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.constants import ParseMode
from telegram.ext import (
    CallbackQueryHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

from conversations.tasks.base import BaseTaskConversation
from internal_requests import service as api_service
from internal_requests.entities import Answer

TYPING_ANSWER = 1


class TaskFiveConversation(BaseTaskConversation):
    """
    Класс для управления диалогом, ответственным за прохождение задания.
    Унаследован от базового BaseTaskConversation с переопределением
     необходимых методов.
    """

    async def show_question(
        self, update: Update, _context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        """Показывает единственный вопрос задания."""
        await update.callback_query.edit_message_reply_markup()
        messages = await api_service.get_messages_with_question(
            task_number=self.task_number, question_number=self.number_of_questions
        )
        await update.effective_message.reply_text(
            text=messages[0].content,
            reply_markup=ForceReply(selective=True),
            parse_mode=ParseMode.HTML,
        )
        return TYPING_ANSWER

    async def handle_user_answer(
        self, update: Update, _context: ContextTypes.DEFAULT_TYPE
    ) -> int:
        """
        Принимает ответ пользователя, записывает ответ в БД и вызывает
         show_notification для оповещения пользователя.
        """
        user_answer = update.message.text
        await api_service.create_answer(
            Answer(
                telegram_id=update.effective_message.chat_id,
                task_number=self.task_number,
                number=self.number_of_questions,
                content=user_answer,
            )
        )
        return await self.show_notification(update, _context)

    async def show_notification(
        self, update: Update, _context: ContextTypes.DEFAULT_TYPE
    ) -> int:
        """
        Оповещает пользователя об успешном сохранении ответа в БД в сообщении
         с кнопкой перехода к следующему заданию и завершает диалог.
        """
        await update.effective_message.reply_text(
            text=self.result_intro,
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
        _context.user_data.clear()
        return ConversationHandler.END

    def set_entry_points(self):
        """Описывает entry_point для входа в диалог: кнопка 'Задача 5'."""
        return [
            CallbackQueryHandler(
                self.show_question, pattern=f"start_task_{self.task_number}"
            )
        ]

    def set_states(self):
        """Управляет ведением диалога."""
        return {
            TYPING_ANSWER: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_user_answer)
            ],
        }
