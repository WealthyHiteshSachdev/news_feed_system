from django.core.management import BaseCommand, CommandError

from insta.services import PostService


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
