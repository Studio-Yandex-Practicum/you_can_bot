import logging
from asyncio import sleep
from typing import Callable, Literal, Optional, TypedDict, cast

from telegram import InlineKeyboardMarkup, Update
from telegram.constants import ChatAction, ParseMode
from telegram.ext import CallbackContext, ConversationHandler

import internal_requests.service as api_service
from conversations.general.decorators import (
    TASK_EXECUTION,
    not_in_conversation,
    set_conversation_name,
)
from conversations.menu.callback_funcs import add_task_number_to_prev_message
from conversations.task_8.keyboards import (
    FIRST_STAGE_END_KEYBOARD,
    FURTHER_ACTIONS_KEYBOARD,
    NEXT_KEYBOARD,
    REPLY_KEYBOARD,
    SECOND_STAGE_END_KEYBOARD,
    TASK_END_KEYBOARD,
)
from conversations.task_8.templates import (
    FINAL_MESSAGE_TEXT,
    RESULT_TEXT,
    TEXT_OF_START_TASK_8,
)
from conversations.tasks.base import TASK_ALREADY_DONE_TEXT
from internal_requests.entities import Answer
from utils.error_handler import error_decorator

_LOGGER = logging.getLogger(__name__)

DELAY_TO_AVOID_FLOOD = 2

(
    TASK_DESCRIPTION_STATE,
    END_STAGE,
    STAGE_1,
    STAGE_2,
    STAGE_3,
    FINAL_STATE,
) = range(1, 7)

CURRENT_TASK = 8
START_QUESTION_NUMBER = 1
FIRST_STAGE_END = 20
SECOND_STAGE_END = FIRST_STAGE_END + FIRST_STAGE_END // 2
TASK_END = SECOND_STAGE_END + FIRST_STAGE_END // 4

FIRST_STAGE_END_MESSAGE = "Начало второго круга задания"
SECOND_STAGE_END_MESSAGE = "Начало последнего круга задания"


class LocationOfChoiceInTask(TypedDict):
    question: int
    choice: Literal["а"] | Literal["б"]


@error_decorator(logger=_LOGGER)
async def show_start_of_task_8_with_task_number(
    update: Update, context: CallbackContext
) -> int:
    return await add_task_number_to_prev_message(
        update=update,
        context=context,
        task_number=CURRENT_TASK,
        start_task_method=show_start_of_task_8,
    )


@error_decorator(logger=_LOGGER)
@not_in_conversation(ConversationHandler.END)
@set_conversation_name(TASK_EXECUTION)
async def show_start_of_task_8(update: Update, context: CallbackContext) -> int:
    """Вывод описания задания 8."""
    query = update.callback_query
    if query is not None:
        await query.message.edit_reply_markup()
    task_status = await api_service.get_user_task_status_by_number(
        task_number=CURRENT_TASK, telegram_id=update.effective_user.id
    )
    if task_status.is_done:
        await update.effective_message.reply_text(
            text=TASK_ALREADY_DONE_TEXT, parse_mode=ParseMode.HTML
        )
        del context.user_data["current_conversation"]
        return ConversationHandler.END
    context.user_data["current_question"] = START_QUESTION_NUMBER
    context.user_data["picked_choices"] = []
    context.user_data["result"] = []
    await update.effective_message.reply_text(
        text=TEXT_OF_START_TASK_8, reply_markup=NEXT_KEYBOARD, parse_mode=ParseMode.HTML
    )
    return TASK_DESCRIPTION_STATE


@error_decorator(logger=_LOGGER)
async def send_first_question(update, context):
    await update.effective_message.edit_reply_markup()
    await _send_question(update, context)
    return STAGE_1


@error_decorator(logger=_LOGGER)
async def send_next_stage_2_message(update, context):
    message = update.effective_message
    await message.edit_reply_markup()
    await message.reply_text(FIRST_STAGE_END_MESSAGE)
    context.user_data["offset"] = FIRST_STAGE_END
    await _send_question(update, context)
    return STAGE_2


@error_decorator(logger=_LOGGER)
async def send_next_stage_3_message(update, context):
    message = update.effective_message
    await message.edit_reply_markup()
    await message.reply_text(SECOND_STAGE_END_MESSAGE)
    context.user_data["offset"] = SECOND_STAGE_END
    await _send_question(update, context)
    return STAGE_3


def handle_answer(
    stage_end: int, end_keyboard: Optional[InlineKeyboardMarkup] = None
) -> Callable:
    def decorator(func):
        async def wrapper(update: Update, context: CallbackContext) -> Optional[int]:
            await update.effective_message.edit_reply_markup()
            picked_choice = await _validate_callback_data(update)
            await _add_answer_to_message(picked_choice, update)
            current_question = context.user_data.get("current_question")
            await func(update, context, current_question, picked_choice)
            if current_question == stage_end:
                context.user_data["current_question"] += 1
                if end_keyboard:
                    await update.effective_message.edit_reply_markup(
                        reply_markup=end_keyboard
                    )
                return END_STAGE
            context.user_data["current_question"] += 1
            await _send_question(update, context)
            return None

        return wrapper

    return decorator


@error_decorator(logger=_LOGGER)
@handle_answer(FIRST_STAGE_END, FIRST_STAGE_END_KEYBOARD)
async def handle_answer_on_stage_1(update, context, current_question, picked_choice):
    await _save_first_stage_answer_to_context(context, current_question, picked_choice)


@error_decorator(logger=_LOGGER)
@handle_answer(SECOND_STAGE_END, SECOND_STAGE_END_KEYBOARD)
async def handle_answer_on_stage_2(update, context, current_question, picked_choice):
    await _save_second_stage_answer_to_context(context, current_question, picked_choice)


@error_decorator(logger=_LOGGER)
@handle_answer(TASK_END, TASK_END_KEYBOARD)
async def handle_answer_on_stage_3(update, context, current_question, picked_choice):
    await _save_third_stage_answer_to_context(context, current_question, picked_choice)
    if current_question == TASK_END:
        await _save_answer_to_db(context, update.effective_chat.id)


@error_decorator(logger=_LOGGER)
async def show_result(update: Update, _context: CallbackContext) -> int:
    """Отправляет результаты прохождения задания."""
    query = update.callback_query
    if query is not None:
        await query.message.edit_reply_markup()

    messages = await api_service.get_messages_with_results(
        telegram_id=update.effective_chat.id, task_number=CURRENT_TASK
    )
    await query.message.reply_text(
        text=RESULT_TEXT,
        parse_mode=ParseMode.HTML,
    )
    for message in messages[:-1]:
        await query.message.reply_text(
            text=message.content,
            parse_mode=ParseMode.HTML,
        )
    await query.message.reply_text(
        text=messages[-1].content,
        parse_mode=ParseMode.HTML,
        reply_markup=FURTHER_ACTIONS_KEYBOARD,
    )
    return FINAL_STATE


@error_decorator(logger=_LOGGER)
async def send_final_message(update: Update, context: CallbackContext) -> int:
    """Отправляет сообщение - поздравление о прохождении всех заданий."""
    await update.effective_message.edit_reply_markup()
    user_info = await api_service.get_info_about_user(
        telegram_id=update.effective_chat.id
    )
    await update.effective_chat.send_message(
        text=FINAL_MESSAGE_TEXT.substitute(name=user_info.name),
        parse_mode=ParseMode.HTML,
    )
    context.user_data.clear()
    return ConversationHandler.END


async def _send_question(update: Update, context: CallbackContext) -> None:
    """Начинает новый вопрос."""
    question_number = context.user_data.get("current_question")
    if FIRST_STAGE_END < question_number:
        params = context.user_data["picked_choices"][
            question_number - FIRST_STAGE_END - 1
        ]
        messages = await api_service.get_task_8_question(
            question_number=(question_number - context.user_data["offset"]),
            params=params,
        )
    else:
        messages = await api_service.get_messages_with_question(
            task_number=CURRENT_TASK,
            question_number=question_number,
        )
    await update.effective_chat.send_action(ChatAction.TYPING)
    await sleep(DELAY_TO_AVOID_FLOOD)
    await update.effective_message.reply_text(
        text=messages[0].content,
        reply_markup=REPLY_KEYBOARD,
        parse_mode=ParseMode.HTML,
    )


async def _add_answer_to_message(picked_choice, update):
    message = update.effective_message
    await message.edit_text(
        text=f"{message.text_html}\n\nОтвет: {picked_choice.upper()}",
        parse_mode=ParseMode.HTML,
    )


async def _validate_callback_data(update: Update) -> Literal["а"] | Literal["б"]:
    picked_choice = update.callback_query.data
    if picked_choice in ["а", "б"]:
        picked_choice = cast(Literal["а"] | Literal["б"], picked_choice)
        return picked_choice
    raise ValueError("Получен некорректный вариант ответа.")


async def _save_first_stage_answer_to_context(
    context: CallbackContext,
    question_number: int,
    picked_choice: Literal["а"] | Literal["б"],
) -> None:
    """Сохраняет выбранные ответы для формирования пар на втором круге."""
    await _save_picked_choice_to_context(
        context=context,
        question_number=question_number,
        picked_choice=LocationOfChoiceInTask(
            question=question_number, choice=picked_choice
        ),
    )


async def _save_second_stage_answer_to_context(
    context: CallbackContext,
    question_number: int,
    picked_choice: Literal["а"] | Literal["б"],
) -> None:
    """Сохраняет выбранные ответы для формирования пар на третьем круге."""
    picked_choice_on_second_stage = await _get_picked_choice_dict_from_context(
        context=context, question_number=question_number, picked_choice=picked_choice
    )
    await _save_picked_choice_to_context(
        context=context,
        question_number=question_number,
        picked_choice=picked_choice_on_second_stage,
    )


async def _save_third_stage_answer_to_context(
    context: CallbackContext,
    question_number: int,
    picked_choice: Literal["а"] | Literal["б"],
) -> None:
    """Сохраняет выбранные ответы для формирования результатов."""
    hidden_talent = await _get_picked_choice_dict_from_context(
        context=context, question_number=question_number, picked_choice=picked_choice
    )
    context.user_data["result"].append(
        f"{hidden_talent['question']}{hidden_talent['choice']}"
    )


async def _save_picked_choice_to_context(
    context: CallbackContext, question_number: int, picked_choice: dict
) -> None:
    """
    Сохраняет выбранный ответ в контекст, формируя пары для вопросов следующих кругов.
    """
    if question_number % 2 == 0:
        last_elem = context.user_data["picked_choices"][-1]
        last_elem.append(picked_choice)
    else:
        context.user_data["picked_choices"].append([picked_choice])


async def _get_picked_choice_dict_from_context(
    context: CallbackContext,
    question_number: int,
    picked_choice: Literal["а"] | Literal["б"],
) -> LocationOfChoiceInTask:
    """Возвращает ответ из прошлых кругов."""
    if picked_choice == "а":
        picked_choice_dict = context.user_data["picked_choices"][
            question_number - FIRST_STAGE_END - 1
        ][0]
    else:
        picked_choice_dict = context.user_data["picked_choices"][
            question_number - FIRST_STAGE_END - 1
        ][1]
    return picked_choice_dict


async def _save_answer_to_db(context: CallbackContext, telegram_id: int):
    await api_service.create_answer(
        Answer(
            telegram_id=telegram_id,
            task_number=CURRENT_TASK,
            number=1,
            content=",".join(context.user_data["result"]),
        )
    )
