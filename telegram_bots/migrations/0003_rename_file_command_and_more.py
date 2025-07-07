from django.db import migrations, models
import django.db.models.deletion

import telegram_bots.models


class Migration(migrations.Migration):
    dependencies = [
        ('telegram_bots', '0002_alter_backgroundtaskapirequest_url_and_more')
    ]
    operations = [
        migrations.RenameField(
            model_name='commandimage', old_name='image', new_name='file'
        ),
        migrations.RenameModel(old_name='CommandFile', new_name='CommandDocument'),
        migrations.AlterModelTable(
            name='commanddocument', table='telegram_bot_command_document'
        ),
        migrations.AlterField(
            model_name='commanddocument',
            name='command',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='documents',
                to='telegram_bots.command',
                verbose_name='Команда',
            ),
        ),
        migrations.AlterField(
            model_name='commanddocument',
            name='file',
            field=models.FileField(
                blank=True,
                max_length=500,
                null=True,
                upload_to=telegram_bots.models.command.upload_command_media_path,
                verbose_name='Документ',
            ),
        ),
        migrations.AlterModelOptions(
            name='commanddocument',
            options={
                'verbose_name': 'Документ команды',
                'verbose_name_plural': 'Документы команд',
            },
        ),
    ]
