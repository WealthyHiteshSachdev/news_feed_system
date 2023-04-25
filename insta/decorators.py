import functools

from django.utils import timezone
from rest_framework.exceptions import ValidationError


def auth_required(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        token = kwargs.get('token')
        if not token:
            raise ValidationError('Please login first')
        from insta.services import SessionService
        session = SessionService.get_session_from_token(token)
        if not session:
            raise ValidationError('Please login first')
        now = timezone.now()
        if session.expires_at <= now:
            raise ValidationError('Session expired. Please login again')
        kwargs['user_id'] = session.user_id
        return func(*args, **kwargs)
    return wrapper
