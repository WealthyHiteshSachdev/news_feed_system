from django.core.management import BaseCommand, CommandError

from insta.services import CommentService


class Command(BaseCommand):
    help = "Comment on post"

    def add_arguments(self, parser):
        parser.add_argument("token", type=str)
        parser.add_argument("post_id", type=str)
        parser.add_argument("text", nargs="+", type=str)

    def handle(self, *args, **options):
        token = options['token']
        post_id = options['post_id']
        text = options['text']
        text = " ".join(text)
        try:
            CommentService.create_comment(token=token, post_id=post_id, text=text)
        except Exception as e:
            raise CommandError(e)
        self.stdout.write(
            self.style.SUCCESS("Comment posted successfully")
        )
