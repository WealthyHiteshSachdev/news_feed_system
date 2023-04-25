from django.core.management import BaseCommand, CommandError

from insta.services import PostService

# eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJleHBpcmVzX2F0IjoiMjAyMy0wNC0yNiAxNzoyMzoyMC4wNjIwOTIrMDA6MDAifQ.qQeJozXO16CkxhHYk9HlM_pHUXb4oonoNlrPBXLkkG4


class Command(BaseCommand):
    help = "Create post"

    def add_arguments(self, parser):
        parser.add_argument("token", type=str)
        parser.add_argument("text", nargs="+", type=str)

    def handle(self, *args, **options):
        token = options['token']
        text = options['text']
        text = " ".join(text)
        try:
            PostService.create_post(token=token, text=text)
        except Exception as e:
            raise CommandError(e)
        self.stdout.write(
            self.style.SUCCESS("Post created successfully")
        )
