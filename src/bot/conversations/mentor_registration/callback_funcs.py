import logging

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

from conversations.general.decorators import not_in_conversation, set_conversation_name
from conversations.mentor_registration.templates import (
    ASK_FIRST_NAME,
    ASK_LAST_NAME,
    CONFIRM_BUTTON,
    CONFIRMATION_REQUEST,
    CONFIRMED,
    LONG_FIRST_NAME_MSG,
    LONG_LAST_NAME_MSG,
    REG_STATUS_CONFIRMED,
    REG_STATUS_NOT_CONFIRMED,
    REGISTRATION_CANCEL,
    REGISTRATION_END,
    REJECT_BUTTON,
    REJECTED,
    SHORT_FIRST_NAME_MSG,
    SHORT_LAST_NAME_MSG,
)
from conversations.menu.cancel_command.handlers import cancel_handler
from internal_requests import service as api_service
from internal_requests.entities import Mentor
from utils.configs import MAIN_MENTOR_ID
from utils.error_handler import error_decorator

TYPING_FIRST_NAME = 1
TYPING_LAST_NAME = 2
MIN_NAME_LENGTH = 2
MAX_NAME_LENGTH = 30
REGISTRATION_CONFIRM = "registration_confirm"
REGISTRATION_REJECT = "registration_reject"

_LOGGER = logging.getLogger(__name__)


class MentorRegistrationConversation:
    """
    Класс для управления диалогом регистрации профдизайнера.
    """

    @not_in_conversation
    @set_conversation_name("mentor_registration")
    @error_decorator(logger=_LOGGER)
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """
        Начало диалога. Проверяет, не был ли пользователь зарегистрирован ранее.
        Переводит диалог в состояние TYPING_FIRST_NAME (ввод имени пользователя).
        """
        registration_status = await api_service.get_mentor_registration_status(
            telegram_id=update.effective_user.id
        )
        if registration_status.registered:
            await update.effective_message.reply_text(
                (
                    REG_STATUS_CONFIRMED
                    if registration_status.confirmed
                    else REG_STATUS_NOT_CONFIRMED
                ),
            )
            context.user_data.clear()
            return ConversationHandler.END
        await update.effective_message.reply_text(ASK_FIRST_NAME)
        return TYPING_FIRST_NAME

    @error_decorator(logger=_LOGGER)
    async def handle_name(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> int:
        """
        Обрабатывает введенное пользователем имя.
        Переводит диалог в состояние TYPING_LAST_NAME (ввод фамилии пользователя).
        """
        first_name = update.message.text.strip()
        if len(first_name) < MIN_NAME_LENGTH:
            await update.effective_message.reply_text(SHORT_FIRST_NAME_MSG)
            return TYPING_FIRST_NAME
        if len(first_name) > MAX_NAME_LENGTH:
            await update.effective_message.reply_text(LONG_FIRST_NAME_MSG)
            return TYPING_FIRST_NAME
        context.user_data["first_name"] = first_name
        await update.effective_message.reply_text(ASK_LAST_NAME)
        return TYPING_LAST_NAME

    @error_decorator(logger=_LOGGER)
    async def handle_surname(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> int:
        """
        Обрабатывает введенную пользователем фамилию.
        Вызывает finish_conversation для регистрации пользователя и завершения диалога.
        """
        last_name = update.message.text.strip()
        if len(last_name) < MIN_NAME_LENGTH:
            await update.effective_message.reply_text(SHORT_LAST_NAME_MSG)
            return TYPING_LAST_NAME
        if len(last_name) > MAX_NAME_LENGTH:
            await update.effective_message.reply_text(LONG_LAST_NAME_MSG)
            return TYPING_LAST_NAME
        context.user_data["last_name"] = last_name
        return await self.finish_conversation(update, context)

    async def finish_conversation(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> int:
        """
        Регистрирует пользователя и выводит сообщение о завершении регистрации.
        Вызывает метод для отправки запроса на подтверждение регистрации,
        после чего завершает диалог.
        """
        mentor = await api_service.create_mentor(
            Mentor(
                first_name=context.user_data.get("first_name"),
                last_name=context.user_data.get("last_name"),
                telegram_id=update.effective_user.id,
            )
        )
        await update.effective_message.reply_text(
            REGISTRATION_END.format(login=mentor.username, password=mentor.password),
        )
        await self.send_confirmation_request(update, context)
        context.user_data.clear()
        return ConversationHandler.END

    async def send_confirmation_request(
        self, update: Update, context: ContextTypes.DEFAULT_TYPE
    ) -> None:
        """
        Отправляет сообщение с запросом на подтверждение регистрации.
        """
        telegram_id = update.effective_user.id
        keyboard = (
            (
                InlineKeyboardButton(
                    text=CONFIRM_BUTTON,
                    callback_data=".".join([REGISTRATION_CONFIRM, str(telegram_id)]),
                ),
            ),
            (
                InlineKeyboardButton(
                    text=REJECT_BUTTON,
                    callback_data=".".join([REGISTRATION_REJECT, str(telegram_id)]),
                ),
            ),
        )
        await context.bot.send_message(
            chat_id=MAIN_MENTOR_ID,
            text=CONFIRMATION_REQUEST.format(
                first_name=context.user_data.get("first_name"),
                last_name=context.user_data.get("last_name"),
                username=update.effective_user.username,
            ),
            reply_markup=InlineKeyboardMarkup(keyboard),
        )

    @error_decorator(logger=_LOGGER)
    async def cancel(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """
        Прерывает процесс регистрации.
        """
        await update.effective_message.reply_text(REGISTRATION_CANCEL)
        context.user_data.clear()
        return ConversationHandler.END

    def set_entry_points(self):
        """
        Описывает entry_points для вхождения в диалог.
        """
        return [CommandHandler("reg", self.start)]

    def set_states(self):
        """
        Управляет ведением диалога.
        """
        return {
            TYPING_FIRST_NAME: [
                MessageHandler(filters.TEXT & (~filters.COMMAND), self.handle_name)
            ],
            TYPING_LAST_NAME: [
                MessageHandler(filters.TEXT & (~filters.COMMAND), self.handle_surname)
            ],
        }

    def set_fallbacks(self):
        """
        Управляет выходом из диалога.
        """
        return [MessageHandler(filters.Regex("/reg"), self.cancel), cancel_handler]

    def add_handlers(self):
        """
        Формирует хэндлер для диалога регистрации профдизайнера.
        """
        return ConversationHandler(
            entry_points=self.set_entry_points(),
            states=self.set_states(),
            fallbacks=self.set_fallbacks(),
        )


async def registration_confirmation(
    update: Update, _context: ContextTypes.DEFAULT_TYPE
) -> None:
    """
    Обрабатывает ответ на запрос подтверждения регистрации.
    В зависимости от полученных в callback_query данных
    либо подтверждает регистрацию профдизайнера,
    либо отклоняет и удаляет его учетную запись.
    """
    try:
        await _process_mentor_registration_confirmation(update)
    except Exception as exc:
        await update.effective_message.reply_text(
            "Что-то пошло не так. "
            "Возможно, потребуется вручную выполнить действие в админке."
        )
        raise exc


async def _process_mentor_registration_confirmation(update):
    await update.callback_query.answer()
    await update.callback_query.edit_message_reply_markup()
    picked_choice = update.callback_query.data
    command, id_to_confirm = picked_choice.split(".")
    id_to_confirm = int(id_to_confirm)
    if command == REGISTRATION_CONFIRM:
        await api_service.confirm_mentor_registration(id_to_confirm)
        await update.effective_message.reply_text(CONFIRMED)
    elif command == REGISTRATION_REJECT:
        await api_service.delete_mentor(id_to_confirm)
        await update.effective_message.reply_text(REJECTED)
