# Generated by Django 4.2.5 on 2024-03-03 19:11

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0024_alter_task_options"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="task",
            options={
                "ordering": ("number",),
                "verbose_name": "Задание",
                "verbose_name_plural": "Задания",
            },
        ),
    ]
