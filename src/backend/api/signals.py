from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from api.models import MentorProfile, Task, TaskStatus, UserFromTelegram

User = get_user_model()


@receiver(post_save, sender=UserFromTelegram)
def create_task_statuses(sender, instance, created, **kwargs):
    if created is True:
        numbers_of_end_questions_in_tasks = {
            Task.TaskNumber.FIRST: 10,
            Task.TaskNumber.SECOND: 70,
            Task.TaskNumber.THIRD: 42,
            Task.TaskNumber.FOURTH: 41,
            Task.TaskNumber.FIFTH: 1,
            Task.TaskNumber.SIXTH: 3,
            Task.TaskNumber.SEVENTH: 1,
            Task.TaskNumber.EIGHTH: 1,
        }
        for task_number in Task.TaskNumber.values:
            task, created = Task.objects.get_or_create(
                number=task_number,
                end_question=numbers_of_end_questions_in_tasks[task_number],
            )
            TaskStatus.objects.create(
                user=instance,
                task=task,
            )


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created is True:
        telegram_id = getattr(instance, "_telegram_id", None)
        MentorProfile.objects.create(user=instance, telegram_id=telegram_id)


@receiver(post_save, sender=TaskStatus)
def update_user_progress_on_task_completion(sender, instance, created, **kwargs):
    """
    Обновляет количество выполненных заданий и дату последнего выполненного задания.
    """
    user = instance.user
    tasks_completed_count = TaskStatus.objects.filter(user=user, is_done=True).count()
    user.tasks_completed_count = tasks_completed_count
    user.last_task_completed_at = instance.pass_date
    user.save()
