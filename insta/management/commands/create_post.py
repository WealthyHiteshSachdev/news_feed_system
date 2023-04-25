from django.core.management import BaseCommand, CommandError

from insta.services import PostService


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
