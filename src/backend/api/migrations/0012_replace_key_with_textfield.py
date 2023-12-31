# Generated by Django 4.2.5 on 2023-10-04 08:40

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0011_alter_result_options_alter_result_unique_together"),
    ]

    operations = [
        migrations.AlterField(
            model_name="result",
            name="key",
            field=models.TextField(
                help_text="Значение, полученное в ходе расшифровки, которое используется как краткая запись результата. Например, ISTP.",
                verbose_name="Ключ",
            ),
        ),
    ]
