from dataclasses import dataclass
from typing import Optional


@dataclass
class Answer:
    telegram_id: int
    task_number: int
    number: int
    content: str


@dataclass
class Problem:
    telegram_id: int
    message: str


@dataclass
class UserFromTelegram:
    telegram_id: int
    telegram_username: str
    name: str
    surname: str


@dataclass
class TaskStatus:
    number: int
    current_question: Optional[int]
    is_done: bool


@dataclass
class Message:
    telegram_id: int
    content: str
    photo: Optional[str]
