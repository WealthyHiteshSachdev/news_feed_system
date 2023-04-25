from django.core.management import BaseCommand, CommandError

from insta.services import PostService

# eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJleHBpcmVzX2F0IjoiMjAyMy0wNC0yNiAxNzoyMzoyMC4wNjIwOTIrMDA6MDAifQ.qQeJozXO16CkxhHYk9HlM_pHUXb4oonoNlrPBXLkkG4


class Command(BaseCommand):
    help = "View available commands for the app"

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        from django.core.management import get_commands
        commands = get_commands()
        commands = [c for c, a in commands.items() if a == 'insta']
        self.stdout.write(
            self.style.SUCCESS(commands)
        )