# Generated by Django 5.0.6 on 2025-02-04 21:15

import constructor_telegram_bots.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('donation', '0002_alter_method_position_alter_section_position'),
    ]

    operations = [
        migrations.AlterField(
            model_name='method',
            name='link',
            field=constructor_telegram_bots.fields.PublicURLField(blank=True, null=True, verbose_name='Ссылка'),
        ),
    ]
