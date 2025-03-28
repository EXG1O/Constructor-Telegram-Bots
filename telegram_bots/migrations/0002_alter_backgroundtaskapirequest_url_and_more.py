# Generated by Django 5.0.6 on 2025-02-04 21:15

import constructor_telegram_bots.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('telegram_bots', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='backgroundtaskapirequest',
            name='url',
            field=constructor_telegram_bots.fields.PublicURLField(verbose_name='URL-адрес'),
        ),
        migrations.AlterField(
            model_name='commandapirequest',
            name='url',
            field=constructor_telegram_bots.fields.PublicURLField(verbose_name='URL-адрес'),
        ),
        migrations.AlterField(
            model_name='commandfile',
            name='from_url',
            field=constructor_telegram_bots.fields.PublicURLField(blank=True, null=True, verbose_name='Из URL-адреса'),
        ),
        migrations.AlterField(
            model_name='commandimage',
            name='from_url',
            field=constructor_telegram_bots.fields.PublicURLField(blank=True, null=True, verbose_name='Из URL-адреса'),
        ),
        migrations.AlterField(
            model_name='commandkeyboardbutton',
            name='url',
            field=constructor_telegram_bots.fields.PublicURLField(blank=True, null=True, verbose_name='URL-адрес'),
        ),
    ]
