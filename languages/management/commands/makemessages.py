from django.conf import settings
from django.core.management.commands import makemessages

from pathlib import Path


class Command(makemessages.Command):
    def find_files(self, root: str) -> list[makemessages.TranslatableFile]:
        result: list[makemessages.TranslatableFile] = super().find_files(root)

        frontend_html_file: Path = settings.FRONTEND_PATH / 'src/prod.html'

        if frontend_html_file.exists():
            result.append(
                self.translatable_file_class(
                    dirpath=str(frontend_html_file.parent),
                    file_name=frontend_html_file.name,
                    locale_dir=self.default_locale_path,
                )
            )

        return result
