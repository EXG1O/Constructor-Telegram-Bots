# Generated by Django 4.2.3 on 2023-09-24 00:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('telegram_bot', '0018_rename_show_in_menu_telegrambotcommandcommand_is_show_in_menu_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='telegrambot',
            name='added_date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Добавлен'),
        ),
    ]
