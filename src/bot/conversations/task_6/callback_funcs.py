from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.constants import ParseMode
from telegram.ext import (
    CallbackQueryHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

from conversations.tasks.base import CHOOSING, NEXT_BUTTON_PATTERN, BaseTaskConversation
from internal_requests import service as api_service
from internal_requests.entities import Answer


class TaskSixConversation(BaseTaskConversation):
    """
    Класс для обработки диалогов в Задании 6.
    Хэндлер для обработки ответов пользователя заменен на MessageHandler,
    пользователь отправляет ответы в виде текстовых сообщений.
    """

    async def show_question(
        self,
        update: Update,
        _context: ContextTypes.DEFAULT_TYPE,
        question_number: int = 1,
    ) -> None:
        """
        Показывает очередной вопрос, относящийся к текущему заданию.
        """
        if question_number == 1:
            await update.callback_query.edit_message_reply_markup()
        messages = await api_service.get_messages_with_question(
            task_number=self.task_number,
            question_number=question_number,
        )
        await update.effective_message.reply_text(
            text=messages[0].content,
            parse_mode=ParseMode.HTML,
        )

    async def show_result(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Выводит результаты пользователя и завершает диалог текущего задания,
        после чего переходит к следующему заданию.
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
        context.user_data.clear()
        return ConversationHandler.END

    async def handle_user_answer(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> int:
        """
        Обрабатывает ответ пользователя на вопрос и вызывает метод show_question,
        чтобы перейти к следующему вопросу. Если вопрос был последний,
        вызывает show_result, чтобы вывести результат пользователя
        и завершить диалог.
        """
        current_question = context.user_data.get("current_question")
        await api_service.create_answer(
            Answer(
                telegram_id=update.effective_message.chat_id,
                task_number=self.task_number,
                number=current_question,
                content=update.message.text,
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

    def set_states(self):
        """
        Управляет ведением диалога.
        Используется при создании хэндлера для задания.
        """
        return {
            CHOOSING: [
                CallbackQueryHandler(self.question_method, pattern=NEXT_BUTTON_PATTERN),
                MessageHandler(filters.TEXT & (~filters.COMMAND), self.update_method),
            ]
        }
