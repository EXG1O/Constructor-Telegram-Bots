from django.db import migrations

from constructor_telegram_bots.migrations import convert_html_to_markdown


class Migration(migrations.Migration):
    dependencies = [('donation', '0003_alter_method_link')]
    operations = [
        migrations.RunPython(
            convert_html_to_markdown(
                app_label='donation', model_name='Section', fields=['text']
            )
        )
    ]
