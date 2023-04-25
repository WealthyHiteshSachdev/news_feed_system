from django.core.management import BaseCommand, CommandError

from insta.services import CommentService


class Command(BaseCommand):
    help = "Upvote comment"

    def add_arguments(self, parser):
        parser.add_argument("token", type=str)
        parser.add_argument("comment_id", type=str)

    def handle(self, *args, **options):
        token = options['token']
        comment_id = options['comment_id']
        try:
            CommentService.upvote(token=token, comment_id=comment_id)
        except Exception as e:
            raise CommandError(e)
        self.stdout.write(
            self.style.SUCCESS("Command processed successfully")
        )
