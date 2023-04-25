from django.core.management import BaseCommand, CommandError

from insta.services import UserService


class Command(BaseCommand):
    help = "User signup"

    def add_arguments(self, parser):
        parser.add_argument("username", type=str)
        parser.add_argument("password", type=str)

    def handle(self, *args, **options):
        username = options['username']
        password = options['password']
        try:
            UserService.signup(username=username, password=password)
        except Exception as e:
            raise CommandError(e)
        self.stdout.write(
            self.style.SUCCESS("Signup successful. You can now login using your credentials")
        )
