from django.core.management import BaseCommand, CommandError

from insta.services import CommentService


class Command(BaseCommand):
    help = "Show post comments"

    def add_arguments(self, parser):
        parser.add_argument("post_id", type=str)

    def handle(self, *args, **options):
        post_id = options['post_id']
        try:
            comments = CommentService.get_post_comments(post_id=post_id)
        except Exception as e:
            raise CommandError(e)
        self.stdout.write(
            self.style.SUCCESS(comments)
        )
