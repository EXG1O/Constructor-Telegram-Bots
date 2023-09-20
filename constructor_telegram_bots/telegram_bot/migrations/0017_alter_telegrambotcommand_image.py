# Generated by Django 4.2.3 on 2023-09-20 01:31

from django.db import migrations, models
import telegram_bot.models


class Migration(migrations.Migration):

    dependencies = [
        ('telegram_bot', '0016_alter_telegrambotcommand_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='telegrambotcommand',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=telegram_bot.models.upload_telegram_bot_command_image_path, verbose_name='Изображение'),
        ),
    ]
