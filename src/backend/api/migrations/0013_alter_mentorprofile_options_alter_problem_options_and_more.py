# Generated by Django 4.2.5 on 2023-10-17 08:24

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0012_replace_key_with_textfield"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="mentorprofile",
            options={
                "verbose_name": "Профиль психолога",
                "verbose_name_plural": "Профили психологов",
            },
        ),
        migrations.AlterModelOptions(
            name="problem",
            options={
                "ordering": ("-pk",),
                "verbose_name": "вопрос",
                "verbose_name_plural": "Вопросы от пользователей",
            },
        ),
        migrations.RemoveField(
            model_name="mentorprofile",
            name="telegram_username",
        ),
        migrations.AddField(
            model_name="mentorprofile",
            name="telegram_id",
            field=models.PositiveIntegerField(
                blank=True,
                help_text="На этот id в Telegram могут быть отправлены уведомления",
                null=True,
                verbose_name="Айди Telegram",
            ),
        ),
    ]