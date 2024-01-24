# Generated by Django 5.0 on 2024-01-22 19:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('donation', '0006_alter_donationbutton_position_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='donation',
            options={'ordering': ('-sum',), 'verbose_name': 'Пожертвование', 'verbose_name_plural': 'Пожертвования'},
        ),
        migrations.AlterModelOptions(
            name='donationbutton',
            options={'ordering': ('position',), 'verbose_name': 'Кнопку', 'verbose_name_plural': 'Кнопки'},
        ),
        migrations.AlterModelOptions(
            name='donationsection',
            options={'ordering': ('position',), 'verbose_name': 'Раздел', 'verbose_name_plural': 'Разделы'},
        ),
    ]