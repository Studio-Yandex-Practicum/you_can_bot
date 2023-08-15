from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Update
)
from telegram.ext import (
    BaseHandler,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    CallbackQueryHandler
)

from templates import MESSAGES

STARTING_RANGE = 5  # Номер первого сообщения, относящегося к этому заданию
MAX_CHOICES = 6  # Количество вариантов ответа в вопросе
MESSAGE_KEY_TEMPLATE = 'message_{}'  # Шаблон ключа для получения информации
NUMBER_OF_QUESTIONS = 10  # Количество вопросов в задании
CHOOSING = 1


def save_answer(user, question_number, answer):
    """Сохраняет ответ пользователя."""
    pass


def make_me_a_keyboard(
        buttons_dict: dict[str, str],
        picked_answers: dict[str, str] = {}
) -> list[InlineKeyboardButton]:
    """Создаёт клавиатуру для текущего сообщения
    с учетом уже выбранных ответов."""
    keyboard = []
    for pos, text in buttons_dict.items():
        if pos not in picked_answers.keys():
            keyboard.append(
                [InlineKeyboardButton(text, callback_data=pos)]
            )
    return keyboard


def question_start(
        context: ContextTypes.DEFAULT_TYPE,
        question_number: int = 1
) -> None:
    """Задаёт стартовые значения параметров для вопроса."""
    context.user_data['current_question'] = question_number
    context.user_data['picked_answers'] = {}


async def start_task_1(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
) -> int:
    """Начальное соостояние задания."""
    start_message_info = MESSAGES[
        MESSAGE_KEY_TEMPLATE.format(STARTING_RANGE)
    ]
    await update.message.reply_text(
        start_message_info['text'],
        reply_markup=InlineKeyboardMarkup(
            make_me_a_keyboard(start_message_info['buttons']),
        ),
    )

    return CHOOSING


async def button(update, context):
    """Запрос информации о выбранном предопределенном выборе."""
    choice = update.callback_query.data
    if choice == 'Начало':
        question_start(context)
    else:
        context.user_data['picked_answers'][
            choice
        ] = MAX_CHOICES-len(context.user_data['picked_answers'])
    if len(context.user_data['picked_answers']) == MAX_CHOICES:
        save_answer(
            update.callback_query.from_user,
            context.user_data['current_question'],
            context.user_data['picked_answers']
        )
        question_start(context, context.user_data['current_question'] + 1)
    query = update.callback_query
    await query.answer()
    current_qestion_key = MESSAGES[
        MESSAGE_KEY_TEMPLATE.format(5+context.user_data['current_question'])
    ]
    if context.user_data['current_question'] == NUMBER_OF_QUESTIONS + 1:
        await query.edit_message_text(
            current_qestion_key['text'],
        )
        return ConversationHandler.END
    await query.edit_message_text(
        current_qestion_key['text'],
        reply_markup=InlineKeyboardMarkup(
            make_me_a_keyboard(
                current_qestion_key['buttons'],
                context.user_data['picked_answers']
            ),
        ),
    )


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Прерывает выполнение задания."""
    await update.message.reply_text(
        'Выполнение задания 1 было пропущено',
    )
    return ConversationHandler.END


def task_1_handler(
        entrypoint: BaseHandler = CommandHandler("start", start_task_1)
) -> None:
    """Возвращает хендлер для первого задания"""

    return ConversationHandler(
        entry_points=[entrypoint],
        states={
            CHOOSING: [
                CallbackQueryHandler(
                    button,
                    pattern=f'^([1-{MAX_CHOICES}]|Начало)$'
                ),
            ],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
