from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from api.models import MentorProfile, TaskStatus, UserFromTelegram

User = get_user_model()


@receiver(post_save, sender=UserFromTelegram)
def create_task_statuses(sender, instance, created, **kwargs):
    if created is True:
        numbers_of_end_questions_in_tasks = {
            TaskStatus.TaskNumber.FIRST: 10,
            TaskStatus.TaskNumber.SECOND: 70,
            TaskStatus.TaskNumber.THIRD: 42,
            TaskStatus.TaskNumber.FOURTH: 41,
            TaskStatus.TaskNumber.FIFTH: 1,
            TaskStatus.TaskNumber.SIXTH: 3,
            TaskStatus.TaskNumber.SEVENTH: 1,
            TaskStatus.TaskNumber.EIGHTH: 20,
        }
        for task_number in TaskStatus.TaskNumber.values:
            TaskStatus.objects.create(
                user=instance,
                number=task_number,
                end_question=numbers_of_end_questions_in_tasks[task_number],
            )


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created is True:
        MentorProfile.objects.create(user=instance)
