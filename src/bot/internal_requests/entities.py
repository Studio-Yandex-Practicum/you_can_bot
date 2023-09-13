from dataclasses import dataclass
from typing import Optional


@dataclass
class Answer:
    telegram_id: int
    task_status: str
    question: str
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
    mentor: str


@dataclass
class TaskStatus:
    telegram_id: int
    task_number: int
    user: str
    task: str
    is_done: bool
    current_question: int
    question_number: int


@dataclass
class Message:
    telegram_id: int
    content: str
    photo: Optional[str]
