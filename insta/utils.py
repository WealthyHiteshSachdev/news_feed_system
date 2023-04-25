import datetime

from django.utils import timezone


thresholds = [
    ("0-59", "sec", "secs", 1),
    ("1-59", "min", "mins", 60),
    ("1-23", "hr", "hrs", 60),
    ("1-30", "day", "days", 24),
    ("1-12", "month", "months", 30),
    ("1-~", "year", "years", 12),
]


def display_time_in_cool_format(timestamp1, timestamp2, prefix=None, postfix=None):
    if not (isinstance(timestamp1, datetime.datetime) and isinstance(timestamp2, datetime.datetime)):
        return
    diff = (timestamp2 - timestamp1).total_seconds()
    for threshold in thresholds:
        limits, specifier1, specifier2, divisor = threshold
        start, end = list(map(int, limits.split('-')))
        diff = int(diff // divisor)
        specifier = specifier2
        output = None
        if end == "~":
            if diff == 1:
                specifier = specifier1
            output = f"{diff} {specifier}"
        elif start <= diff <= end:
            if diff == 1:
                specifier = specifier1
            output = f"{diff} {specifier}"
        if output:
            if prefix:
                output = f"{prefix} {output}"
            if postfix:
                output = f"{output} {postfix}"
            return output
    return timestamp1
