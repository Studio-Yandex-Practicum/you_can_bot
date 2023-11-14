import logging
from asyncio import sleep
from typing import Literal, TypedDict, cast

from telegram import Message, Update
from telegram.constants import ChatAction, ParseMode
from telegram.ext import CallbackContext, ConversationHandler

import internal_requests.service as api_service
from conversations.task_8.keyboards import NEXT_KEYBOARD, REPLY_KEYBOARD
from conversations.task_8.templates import (
    FINAL_MESSAGE_TEXT,
    RESULT_TEXT,
    TEXT_OF_START_TASK_8,
)
from internal_requests.entities import Answer

_LOGGER = logging.getLogger(__name__)

DELAY_TO_AVOID_FLOOD = 3
DELAY_BEFORE_THE_FINAL_MESSAGE = 5

NEXT, CHOOSING = 1, 2

CURRENT_TASK = 8
START_QUESTION_NUMBER = 1
FIRST_STAGE_END = 20
SECOND_STAGE_END = 30
TASK_END = 35


class LocationOfChoiceInTask(TypedDict):
    question: int
    choice: Literal["а"] | Literal["б"]


async def show_start_of_task_8(update: Update, context: CallbackContext) -> int:
    """Вывод описания задания 8."""
    query = update.callback_query
    if query is not None:
        await query.message.edit_reply_markup()
    context.user_data["current_question"] = START_QUESTION_NUMBER
    context.user_data["picked_choices"] = []
    context.user_data["result"] = []
    await update.effective_message.reply_text(
        text=TEXT_OF_START_TASK_8,
        reply_markup=NEXT_KEYBOARD,
    )
    return NEXT


async def start_question(
    update: Update, context: CallbackContext, question_number: int = 1
) -> int:
    """Начинает новый вопрос."""
    query = update.callback_query
    if question_number == 1:
        await query.message.edit_reply_markup()
    if FIRST_STAGE_END < question_number:
        params = context.user_data["picked_choices"][
            question_number - FIRST_STAGE_END - 1
        ]
        messages = await api_service.get_task_8_question(
            question_number=question_number, params=params
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
    return CHOOSING


async def update_question(update: Update, context: CallbackContext) -> int:
    """Обработчик ответов на вопросы."""
    current_question = context.user_data.get("current_question")
    picked_choice = await _validate_callback_data(update)
    message = update.effective_message

    if FIRST_STAGE_END < current_question <= SECOND_STAGE_END:
        await _handle_second_stage_answer(context, current_question, picked_choice)
    elif SECOND_STAGE_END < current_question:
        await _handle_third_stage_answer(context, current_question, picked_choice)
    else:
        await _handle_first_stage_answer(context, current_question, picked_choice)

    await message.edit_text(
        text=f"{message.text_html}\n\nОтвет: {picked_choice.upper()}",
        parse_mode=ParseMode.HTML,
    )

    if current_question == TASK_END:
        await _save_answer_to_db(context, message)
        state = await show_result(update, context)
        return state

    context.user_data["current_question"] += 1
    state = await start_question(
        update, context, context.user_data.get("current_question")
    )
    return state


async def show_result(update: Update, context: CallbackContext) -> int:
    """Отправляет результаты прохождения задания."""
    context.user_data.clear()
    query = update.callback_query
    messages = await api_service.get_messages_with_results(
        telegram_id=update.effective_chat.id, task_number=CURRENT_TASK
    )
    await query.message.reply_text(
        text=RESULT_TEXT,
        parse_mode=ParseMode.HTML,
    )
    for message in messages:
        await query.message.reply_text(
            text=message.content,
            parse_mode=ParseMode.HTML,
        )
    await _send_final_message(update)
    return ConversationHandler.END


async def _validate_callback_data(update: Update) -> Literal["а"] | Literal["б"]:
    picked_choice = update.callback_query.data
    if picked_choice in ["а", "б"]:
        picked_choice = cast(Literal["а"] | Literal["б"], picked_choice)
        return picked_choice
    raise ValueError("Получен некорректный вариант ответа.")


async def _handle_first_stage_answer(
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


async def _handle_second_stage_answer(
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


async def _handle_third_stage_answer(
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


async def _save_answer_to_db(context: CallbackContext, message: Message):
    await api_service.create_answer(
        Answer(
            telegram_id=message.chat_id,
            task_number=CURRENT_TASK,
            number=1,
            content=",".join(context.user_data["result"]),
        )
    )


async def _send_final_message(update: Update) -> None:
    """Отправляет сообщение - поздравление о прохождении всех заданий."""
    await update.effective_chat.send_action(ChatAction.TYPING)
    user_info = await api_service.get_info_about_user(
        telegram_id=update.effective_chat.id
    )
    await sleep(DELAY_BEFORE_THE_FINAL_MESSAGE)
    await update.effective_chat.send_message(
        text=FINAL_MESSAGE_TEXT.substitute(name=user_info.name),
        parse_mode=ParseMode.HTML,
    )
