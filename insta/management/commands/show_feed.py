from django.core.management import BaseCommand, CommandError

from insta.services import FeedService


class Command(BaseCommand):
    help = "Show user feed. Use sort_by and sort_order optional arguments to sort the posts. " \
           "Valid values for sort_by are 'score', 'comments', 'timestamp'. " \
           "Valid values for sort_order are 'asc', 'desc'. " \
           "Ex: python manage.py show_feed {token} --sort_by score --sort_order desc"

    def add_arguments(self, parser):
        parser.add_argument("token", type=str)
        parser.add_argument("--sort_by", type=str)
        parser.add_argument("--sort_order", type=str)

    def handle(self, *args, **options):
        token = options['token']
        sort_by = options.get('sort_by')
        sort_order = options.get('sort_order')
        try:
            feed = FeedService.get_feed(token=token, sort_by=sort_by, sort_order=sort_order)
        except Exception as e:
            raise CommandError(e.args[0])
        self.stdout.write(
            self.style.SUCCESS(feed)
        )


"""
    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument("poll_ids", nargs="+", type=int)

        # Named (optional) arguments
        parser.add_argument(
            "--delete",
            action="store_true",
            help="Delete poll instead of closing it",
        )

    def handle(self, *args, **options):
        # ...
        if options["delete"]:
            poll.delete()
        # ...

"""