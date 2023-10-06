# Generated by Django 4.2.5 on 2023-09-17 04:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0009_alter_question_options_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="answer",
            name="question",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="answers",
                to="api.question",
                verbose_name="Вопрос",
            ),
        ),
    ]