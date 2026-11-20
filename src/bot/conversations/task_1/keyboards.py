"""Keyboards specific to Task 1 (ranking six statements by attractiveness)."""

from typing import Tuple

from telegram import InlineKeyboardButton, InlineKeyboardMarkup

TASK_1_CALLBACK_PATTERN = r"^([А-Е]|slot_[1-6]|undo|confirm)$"

UNDO_CALLBACK = "undo"
CONFIRM_CALLBACK = "confirm"
SLOT_CALLBACK_PREFIX = "slot_"

SLOT_LABELS: Tuple[str, ...] = ("1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣")
EMPTY_SLOT_PLACEHOLDER = "?"
UNDO_BUTTON_LABEL = "↩️ Шаг назад"
CONFIRM_BUTTON_LABEL = "✅ Готово"
CONFIRM_BUSY_LABEL = "⏳ Сохраняю..."


def get_task_1_keyboard(
    choices: Tuple[str, ...],
    picked_choices: str = "",
    committing: bool = False,
) -> InlineKeyboardMarkup:
    """
    Build the three-row inline keyboard for Task 1.

    Row 1: six rank slots (gold, silver, bronze, 4, 5, 6) showing either the
    placed letter or a placeholder.
    Row 2: the unpicked letters from ``choices``.
    Row 3: control buttons — undo (only while 0 < picked < 6) and confirm
    (active only at picked == 6).
    """
    keyboard = [_slot_row(choices, picked_choices)]
    letter_row = _letter_row(choices, picked_choices)
    if letter_row:
        keyboard.append(letter_row)
    control_row = _control_row(choices, picked_choices, committing)
    if control_row:
        keyboard.append(control_row)
    return InlineKeyboardMarkup(keyboard)


def _slot_row(
    choices: Tuple[str, ...], picked_choices: str
) -> list:
    """Render the rank-slot row, filling slots with picked letters in order."""
    row = []
    for index, slot_label in enumerate(SLOT_LABELS[: len(choices)]):
        placed = picked_choices[index] if index < len(picked_choices) else None
        text = (
            f"{slot_label} {placed}"
            if placed is not None
            else f"{slot_label} {EMPTY_SLOT_PLACEHOLDER}"
        )
        row.append(
            InlineKeyboardButton(
                text=text, callback_data=f"{SLOT_CALLBACK_PREFIX}{index + 1}"
            )
        )
    return row


def _letter_row(choices: Tuple[str, ...], picked_choices: str) -> list:
    """Render the row with only the still-unpicked letters."""
    return [
        InlineKeyboardButton(text=label, callback_data=label)
        for label in choices
        if label not in picked_choices
    ]


def _control_row(
    choices: Tuple[str, ...], picked_choices: str, committing: bool
) -> list:
    """Render the undo/confirm controls when applicable."""
    row = []
    picked_count = len(picked_choices)
    total = len(choices)
    if 0 < picked_count < total:
        row.append(
            InlineKeyboardButton(
                text=UNDO_BUTTON_LABEL, callback_data=UNDO_CALLBACK
            )
        )
    if picked_count == total:
        label = CONFIRM_BUSY_LABEL if committing else CONFIRM_BUTTON_LABEL
        row.append(
            InlineKeyboardButton(text=label, callback_data=CONFIRM_CALLBACK)
        )
    return row
