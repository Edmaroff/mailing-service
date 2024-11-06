from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Загружает фикстуры для тестирования приложения"

    def handle(self, *args, **options):
        fixture_files = [
            "apps/mailing/fixtures/tags.json",
            "apps/mailing/fixtures/operator_codes.json",
            "apps/mailing/fixtures/clients.json",
        ]

        for fixture in fixture_files:
            try:
                self.stdout.write(self.style.NOTICE(f"Загрузка {fixture}..."))
                call_command("loaddata", fixture)
                self.stdout.write(self.style.SUCCESS(f"{fixture} загружен успешно"))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Ошибка загрузки {fixture}: {e}"))
