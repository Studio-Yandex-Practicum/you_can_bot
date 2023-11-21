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
    is_done: bool
    current_question: Optional[int] = None


@dataclass
class Message:
    content: str
    photo: str
    telegram_id: Optional[int] = None


@dataclass
class Mentor:
    first_name: str
    last_name: str
    telegram_id: int


@dataclass
class MentorRegistered(Mentor):
    username: str
    password: str


@dataclass
class MentorRegistrationStatus:
    registered: bool
    confirmed: bool
