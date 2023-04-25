from django.core.management import BaseCommand, CommandError

from insta.services import CommentService


class Command(BaseCommand):
    help = "Reply on comment"

    def add_arguments(self, parser):
        parser.add_argument("token", type=str)
        parser.add_argument("comment_id", type=str)
        parser.add_argument("text", nargs="+", type=str)

    def handle(self, *args, **options):
        token = options['token']
        comment_id = options['comment_id']
        text = options['text']
        text = " ".join(text)
        try:
            CommentService.reply_on_comment(token=token, comment_id=comment_id, text=text)
        except Exception as e:
            raise CommandError(e.args[0])
        self.stdout.write(
            self.style.SUCCESS("Replied successfully")
        )
