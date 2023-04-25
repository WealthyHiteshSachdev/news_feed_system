from django.core.management import BaseCommand, CommandError

from insta.services import PostService


class Command(BaseCommand):
    help = "Upvote post"

    def add_arguments(self, parser):
        parser.add_argument("token", type=str)
        parser.add_argument("post_id", type=str)

    def handle(self, *args, **options):
        token = options['token']
        post_id = options['post_id']
        try:
            PostService.upvote(token=token, post_id=post_id)
        except Exception as e:
            raise CommandError(e.args[0])
        self.stdout.write(
            self.style.SUCCESS("Up voted on post successfully")
        )
