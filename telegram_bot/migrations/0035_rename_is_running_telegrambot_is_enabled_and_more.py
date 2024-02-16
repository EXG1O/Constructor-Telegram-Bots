# Generated by Django 5.0 on 2024-02-16 15:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('telegram_bot', '0034_remove_telegrambot_memory_limit_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='telegrambot',
            old_name='is_running',
            new_name='is_enabled',
        ),
        migrations.RemoveField(
            model_name='telegrambot',
            name='is_stopped',
        ),
        migrations.AddField(
            model_name='telegrambot',
            name='is_loading',
            field=models.BooleanField(default=False, verbose_name='Загружаеться'),
        ),
    ]
