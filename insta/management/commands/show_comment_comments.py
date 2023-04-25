from django.core.management import BaseCommand, CommandError

from insta.services import CommentService


class Command(BaseCommand):
    help = "Show comment comments"

    def add_arguments(self, parser):
        parser.add_argument("comment_id", type=str)

    def handle(self, *args, **options):
        comment_id = options['comment_id']
        try:
            comments = CommentService.get_comment_comments(comment_id=comment_id)
        except Exception as e:
            raise CommandError(e)
        self.stdout.write(
            self.style.SUCCESS(comments)
        )
