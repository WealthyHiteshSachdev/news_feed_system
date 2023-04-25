from django.core.management import BaseCommand, CommandError

from insta.services import UserService


class Command(BaseCommand):
    help = "Follow User"

    def add_arguments(self, parser):
        parser.add_argument("token", type=str)
        parser.add_argument("followed_id", type=str)

    def handle(self, *args, **options):
        token = options['token']
        followed_id = options['followed_id']
        try:
            UserService.follow(token=token, followed_id=followed_id)
        except Exception as e:
            raise CommandError(e.args[0])
        self.stdout.write(
            self.style.SUCCESS("Followed successfully")
        )
