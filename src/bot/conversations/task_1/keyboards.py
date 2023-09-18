from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup


def get_inline_keyboard(
    buttons_dict: dict[str, str], picked_choices: str = ""
) -> InlineKeyboardMarkup:
    """Добавляет кнопки в сообщении с учетом уже выбранных ответов."""
    keyboard = []
    for label, text in buttons_dict.items():
        if label not in picked_choices:
            keyboard.append(InlineKeyboardButton(label, callback_data=label))
    return InlineKeyboardMarkup([keyboard])


def get_reply_keyboard(
    buttons_dict: dict[str, str],
) -> ReplyKeyboardMarkup:
    """Создаёт клавиатуру для текущего сообщения."""
    return ReplyKeyboardMarkup(
        [[label for label in buttons_dict]],
        resize_keyboard=True,
        one_time_keyboard=True,
    )
