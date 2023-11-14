from functools import wraps

from telegram import Update
from telegram.ext import ContextTypes

from conversations.general.templates import (
    COMMAND_PROHIBITED,
    COMMAND_PROHIBITED_ON_TASK,
)

TASK_EXECUTION = "task_execution"


def set_conversation_name(conversation_name: str):
    """
    Устанваливает в `context.user_data["current_conversation"]` полученное
    значение `conversation_name`.

    Декоратор используется на функциях, служащих энтрипоинтами для ConversationHandler.
    В дальнейшем значение `context.user_data["current_conversation"]` используется
    для проверки в декораторе `not_in_conversation`.

    Важно: ConversationHandler, для которых использовался этот декоратор, по завершении
    работы должны удалять значение `context.user_data["current_conversation"]` с помощью

    `context.user_data.clear()` или `del context.user_data["current_conversation"]`.
    """

    def decorator(func):
        @wraps(func)
        async def wrapper(*args):
            context: ContextTypes.DEFAULT_TYPE
            if len(args) == 3:
                _instance, _update, context = args
            else:
                _update, context = args
            context.user_data["current_conversation"] = conversation_name
            return await func(*args)

        return wrapper

    return decorator


def not_in_conversation(interrupt_value: int | None = None):
    """
    Проверяет отсутствие активных ConversationHandler, для которых в
    `context.user_data["current_conversation"]` установлено значение.

    Если обнраужено активное обсуждение, прерывает выполнение функции
    и возвращает значение interrupt_value.
    """

    def decorator(func):
        @wraps(func)
        async def wrapper(*args):
            update: Update
            context: ContextTypes.DEFAULT_TYPE
            if len(args) == 3:
                _instance, update, context = args
            else:
                update, context = args
            current_conversation = context.user_data.get("current_conversation")
            if current_conversation:
                await update.effective_message.reply_text(
                    COMMAND_PROHIBITED_ON_TASK
                    if current_conversation == TASK_EXECUTION
                    else COMMAND_PROHIBITED
                )
                return interrupt_value
            return await func(*args)

        return wrapper

    return decorator
