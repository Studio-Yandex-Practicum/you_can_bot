import logging

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import ContextTypes, ConversationHandler

from keyboards import (
    ANSWER, CANSEL, INPUT_PLACEHOLDER, NEXT_KEYBOARD, NEXT_PLACEHOLDER,
    REPLY_KEYBOARD
)
from templates import DESCRIPTION_MESSAGE, MESSAGES, START, STOP


FIRST_QUESTION_MARKER = 'Первый вопрос'
OTHER_QUESTIONS_MARKER = 'Следующий вопрос'
DESCRIPTION_MARKER = 'Последний вопрос'
LAST_MESSAGE = len(MESSAGES) - 1


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)


async def start(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    """Вступление."""
    await update.message.reply_text(
        START,
        reply_markup=ReplyKeyboardMarkup(
            NEXT_KEYBOARD,
            one_time_keyboard=True,
            resize_keyboard=True,
            input_field_placeholder=NEXT_PLACEHOLDER
        ),
    )
    return FIRST_QUESTION_MARKER


async def show_question(
    update: Update, context: ContextTypes.DEFAULT_TYPE,
) -> str:
    """Обработчик вопросов."""
    current_question = context.user_data.get('current_question', 0)
    if current_question != 0:
        logger.info(
            ANSWER,
            update.message.from_user.username,
            current_question - 1,
            update.message.text
        )
    await update.message.reply_text(
        f'{current_question + 1}. {MESSAGES[current_question]}',
        reply_markup=ReplyKeyboardMarkup(
            REPLY_KEYBOARD,
            one_time_keyboard=True,
            resize_keyboard=True,
            input_field_placeholder=INPUT_PLACEHOLDER,
        )
    )
    if current_question == LAST_MESSAGE:
        context.user_data.clear()
        return DESCRIPTION_MARKER
    current_question += 1
    context.user_data['current_question'] = current_question
    return OTHER_QUESTIONS_MARKER


async def description(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> str:
    """Расшифровка."""
    logger.info(
        ANSWER,
        update.message.from_user.username,
        LAST_MESSAGE,
        update.message.text
    )
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=DESCRIPTION_MESSAGE
    )
    return ConversationHandler.END

async def cancel(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Конец диалога."""
    logger.info(CANSEL, update.message.from_user.first_name)
    context.user_data.clear()
    await update.message.reply_text(
        STOP,
        reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END
