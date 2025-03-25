from django.db import migrations

from constructor_telegram_bots.migrations import convert_html_to_markdown


class Migration(migrations.Migration):
    dependencies = [('updates', '0001_initial')]
    operations = [
        migrations.RunPython(
            convert_html_to_markdown(
                app_label='updates', model_name='Update', fields=['description']
            )
        )
    ]
