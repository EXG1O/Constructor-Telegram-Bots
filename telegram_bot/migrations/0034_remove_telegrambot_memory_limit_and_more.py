# Generated by Django 5.0 on 2024-02-09 14:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('telegram_bot', '0033_telegrambot_memory_limit'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='telegrambot',
            name='memory_limit',
        ),
        migrations.AddField(
            model_name='telegrambot',
            name='storage_size',
            field=models.BigIntegerField(default=41943040, verbose_name='Размер хранилища'),
        ),
    ]