from django.core.management import BaseCommand, CommandError

from insta.services import UserService


# hitesh: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJleHBpcmVzX2F0IjoiMjAyMy0wNC0yNiAxNzozMjo1NS4wMjgyOTIrMDA6MDAifQ.fYaY9OlWgfmn0Z-jQHf3tWppuljcQH3qyH6Kr3wu178
# krishna: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoyLCJleHBpcmVzX2F0IjoiMjAyMy0wNC0yNiAxNzo0MTowMC4wMDQzNTUrMDA6MDAifQ.iZiGy4ydALnP3YdZJA5CnotW3mykaDZfj4KaeoM6x8E

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
            raise CommandError(e)
        self.stdout.write(
            self.style.SUCCESS("Followed successfully")
        )
