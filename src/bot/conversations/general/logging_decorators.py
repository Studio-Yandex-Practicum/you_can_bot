import functools
import logging
from typing import Any, Callable

from telegram import Update


def log_decorator(
    logger: logging.Logger,
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @functools.wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            update = next((arg for arg in args if isinstance(arg, Update)), None)

            if update:
                chat_id = getattr(update.effective_chat, "id", "unknown")
                logger.info(
                    "Вызвана функция %s для пользователя %d",
                    func.__name__,
                    chat_id,
                )
            else:
                logger.warning(
                    "При логировании функции %s не удалось получить экземпляр Update",
                    func.__name__,
                )

            return await func(*args, **kwargs)

        return wrapper

    return decorator
