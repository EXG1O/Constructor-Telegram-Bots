from django.db import migrations

from constructor_telegram_bots.migrations import convert_html_to_markdown


class Migration(migrations.Migration):
    dependencies = [('privacy_policy', '0002_alter_section_position')]
    operations = [
        migrations.RunPython(
            convert_html_to_markdown(
                app_label='privacy_policy', model_name='Section', fields=['text']
            )
        )
    ]
