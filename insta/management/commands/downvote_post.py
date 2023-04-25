from django.core.management import BaseCommand, CommandError

from insta.services import PostService


class Command(BaseCommand):
    help = "Downvote post"

    def add_arguments(self, parser):
        parser.add_argument("token", type=str)
        parser.add_argument("post_id", type=str)

    def handle(self, *args, **options):
        token = options['token']
        post_id = options['post_id']
        try:
            PostService.downvote(token=token, post_id=post_id)
        except Exception as e:
            raise CommandError(e)
        self.stdout.write(
            self.style.SUCCESS("Down voted on post successfully")
        )
