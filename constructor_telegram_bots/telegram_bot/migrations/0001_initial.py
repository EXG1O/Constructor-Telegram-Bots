# Generated by Django 4.2.1 on 2023-05-11 20:37

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TelegramBotCommand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('command', models.CharField(max_length=32, null=True)),
                ('callback', models.CharField(max_length=64, null=True)),
                ('message_text', models.TextField()),
                ('keyboard', models.JSONField()),
            ],
            options={
                'db_table': 'telegram_bot_command',
            },
        ),
        migrations.CreateModel(
            name='TelegramBotUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.BigIntegerField()),
                ('username', models.CharField(max_length=32)),
                ('is_allowed', models.BooleanField(default=False)),
                ('date_started', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'telegram_bot_user',
            },
        ),
        migrations.CreateModel(
            name='TelegramBot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, unique=True)),
                ('api_token', models.CharField(max_length=50, unique=True)),
                ('is_private', models.BooleanField(default=True)),
                ('is_running', models.BooleanField(default=False)),
                ('is_stopped', models.BooleanField(default=True)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('commands', models.ManyToManyField(related_name='commands', to='telegram_bot.telegrambotcommand')),
                ('users', models.ManyToManyField(related_name='users', to='telegram_bot.telegrambotuser')),
            ],
            options={
                'db_table': 'telegram_bot',
            },
        ),
    ]
