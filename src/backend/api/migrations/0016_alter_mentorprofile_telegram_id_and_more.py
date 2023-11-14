# Generated by Django 4.2.5 on 2023-11-11 11:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("api", "0015_change_meta_options_on_photo_question_resultstatus_task"),
    ]

    operations = [
        migrations.AlterField(
            model_name="mentorprofile",
            name="telegram_id",
            field=models.PositiveBigIntegerField(
                blank=True,
                help_text="На этот id в Telegram могут быть отправлены уведомления",
                null=True,
                unique=True,
                verbose_name="Айди Telegram",
            ),
        ),
        migrations.AlterField(
            model_name="mentorprofile",
            name="user",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="mentorprofile",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]