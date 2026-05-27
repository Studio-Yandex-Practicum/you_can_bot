"""Conversation callbacks for Task 1 — ranking statements А-Е by attractiveness.

The UI principle here is that the question text is rendered exactly once via
``reply_text`` and is **never** edited afterwards. The full ordering state lives
in ``context.user_data['picked_choices']`` and the keyboard is the only thing
that gets updated as the user picks letters.
"""

import logging

from telegram import Update
from telegram.error import BadRequest
from telegram.ext import CallbackQueryHandler, ContextTypes

from conversations.task_1.keyboards import (
    CONFIRM_CALLBACK,
    SLOT_CALLBACK_PREFIX,
    TASK_1_CALLBACK_PATTERN,
    UNDO_CALLBACK,
    get_task_1_keyboard,
)
from conversations.tasks.base import BaseTaskConversation
from conversations.tasks.keyboards import (
    NEXT_BUTTON_PATTERN,
    SHOW_RESULTS_BUTTON,
)
from conversations.tasks.states import CHOOSING, LAST_QUESTION
from internal_requests import service as api_service
from internal_requests.entities import Answer
from utils.error_handler import error_decorator

MAX_SCORE = 5

PICKED_CHOICES_KEY = "picked_choices"
COMMITTING_KEY = "committing"

_LOGGER = logging.getLogger(__name__)


class TaskOneConversation(BaseTaskConversation):
    """
    Conversation handlers for Task 1.

    Overrides ``show_question`` to render the question once with the Task 1
    specific three-row keyboard, and ``handle_user_answer`` to dispatch every
    callback (letter / slot / undo / confirm) without ever editing the message
    text.
    """

    @error_decorator(logger=_LOGGER)
    async def show_question(
        self,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
    ) -> None:
        """Post the next question as a fresh message with an empty ranking keyboard."""
        current_question = context.user_data["current_question"]
        if current_question == 1 and update.callback_query is not None:
            await self._safe_edit_markup(update.callback_query, reply_markup=None)
        context.user_data[PICKED_CHOICES_KEY] = ""
        context.user_data[COMMITTING_KEY] = False
        messages = await api_service.get_messages_with_question(
            task_number=self.task_number,
            question_number=current_question,
        )
        await update.effective_message.reply_text(
            text=messages[0].content,
            reply_markup=get_task_1_keyboard(self.choices),
        )

    @error_decorator(logger=_LOGGER)
    async def handle_user_answer(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> int:
        """Dispatch a callback from the Task 1 keyboard to the right handler."""
        query = update.callback_query
        context.user_data[COMMITTING_KEY] = False
        data = query.data
        if data == CONFIRM_CALLBACK:
            return await self._handle_confirm(update, context)
        if data == UNDO_CALLBACK:
            return await self._handle_undo(update, context)
        if data.startswith(SLOT_CALLBACK_PREFIX):
            return await self._handle_slot_tap(update, context, data)
        return await self._handle_letter_tap(update, context, data)

    async def _handle_letter_tap(
        self,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
        letter: str,
    ) -> int:
        """Place a tapped letter into the next free slot, if any."""
        picked = context.user_data.get(PICKED_CHOICES_KEY, "")
        if letter in picked or len(picked) >= len(self.choices):
            return CHOOSING
        picked += letter
        context.user_data[PICKED_CHOICES_KEY] = picked
        await self._refresh_keyboard(update, context)
        return CHOOSING

    async def _handle_slot_tap(
        self,
        update: Update,
        context: ContextTypes.DEFAULT_TYPE,
        data: str,
    ) -> int:
        """Tap on a filled slot removes that letter; on an empty slot — ignore."""
        slot_index = int(data[len(SLOT_CALLBACK_PREFIX):]) - 1
        picked = context.user_data.get(PICKED_CHOICES_KEY, "")
        if slot_index >= len(picked):
            return CHOOSING
        picked = picked[:slot_index] + picked[slot_index + 1:]
        context.user_data[PICKED_CHOICES_KEY] = picked
        await self._refresh_keyboard(update, context)
        return CHOOSING

    async def _handle_undo(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> int:
        """Drop the last placed letter."""
        picked = context.user_data.get(PICKED_CHOICES_KEY, "")
        if not picked:
            return CHOOSING
        context.user_data[PICKED_CHOICES_KEY] = picked[:-1]
        await self._refresh_keyboard(update, context)
        return CHOOSING

    async def _handle_confirm(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> int:
        """Persist the final ranking and move on to the next question."""
        picked = context.user_data.get(PICKED_CHOICES_KEY, "")
        if len(picked) != len(self.choices):
            return CHOOSING
        if context.user_data.get(COMMITTING_KEY):
            return CHOOSING
        context.user_data[COMMITTING_KEY] = True
        message = update.effective_message
        current_question = context.user_data.get("current_question")
        try:
            await self._save_answer(message.chat_id, current_question, picked)
        except Exception:
            context.user_data[COMMITTING_KEY] = False
            raise
        _LOGGER.info(
            "Пользователь %d ответил на вопрос №%d Задания №%d",
            message.chat_id,
            current_question,
            self.task_number,
        )
        final_text = f"{message.text_html}\n\n<b>Твой ответ:</b> {picked}"
        if current_question == self.number_of_questions:
            await self._safe_edit_text(
                update.callback_query,
                text=final_text,
                reply_markup=SHOW_RESULTS_BUTTON,
            )
            return LAST_QUESTION
        await self._safe_edit_text(
            update.callback_query, text=final_text, reply_markup=None
        )
        context.user_data["current_question"] += 1
        await self.show_question(update, context)
        return CHOOSING

    async def _refresh_keyboard(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        """Rebuild and apply the keyboard from the current ``picked_choices``."""
        picked = context.user_data.get(PICKED_CHOICES_KEY, "")
        committing = bool(context.user_data.get(COMMITTING_KEY))
        markup = get_task_1_keyboard(
            self.choices, picked_choices=picked, committing=committing
        )
        await self._safe_edit_markup(update.callback_query, reply_markup=markup)

    async def _save_answer(self, user_id, current_question, picked_choices):
        """Save the user's ranking as a 6-digit string of scores 5..0."""
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
    async def _safe_edit_markup(query, reply_markup) -> None:
        """Edit the message reply markup, swallowing 'not modified' errors."""
        if query is None:
            return
        try:
            await query.edit_message_reply_markup(reply_markup=reply_markup)
        except BadRequest as exc:
            if "not modified" in str(exc).lower():
                _LOGGER.debug("Идемпотентный edit_message_reply_markup: %s", exc)
                return
            raise

    @staticmethod
    async def _safe_edit_text(query, text, reply_markup) -> None:
        """Edit message text + markup, swallowing 'not modified' errors."""
        if query is None:
            return
        try:
            await query.edit_message_text(text=text, reply_markup=reply_markup)
        except BadRequest as exc:
            if "not modified" in str(exc).lower():
                _LOGGER.debug("Идемпотентный edit_message_text: %s", exc)
                return
            raise

    def set_states(self):
        """Override the CHOOSING state to use the Task 1 callback vocabulary."""
        states = super().set_states()
        states[CHOOSING] = [
            CallbackQueryHandler(
                self.question_method, pattern=NEXT_BUTTON_PATTERN
            ),
            CallbackQueryHandler(
                self.update_method, pattern=TASK_1_CALLBACK_PATTERN
            ),
        ]
        return states
