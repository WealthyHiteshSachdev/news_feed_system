import datetime

import jwt
from django.db import transaction
from django.db.models import F
from django.utils import timezone
from rest_framework.exceptions import ValidationError

from insta.decorators import auth_required
from insta.models import User, Session, Post, Comment, Follow


class SessionService:
    secret_key = '$ecReTC0dEAn0NYmOu$'

    @classmethod
    def get_jwt_token(cls, data):
        if not data:
            return
        return jwt.encode(data, cls.secret_key, algorithm='HS256')

    @classmethod
    def decode_jwt_token(cls, jwt_token):
        return jwt.decode(jwt_token, cls.secret_key, algorithms=['HS256'])

    @classmethod
    def get_active_session(cls, user_id):
        now = timezone.now()
        return Session.objects.filter(user_id=user_id, expires_at__gt=now).first()

    @classmethod
    def get_session_from_token(cls, token):
        if not token:
            return
        return Session.objects.filter(token=token).first()

    @classmethod
    def create_session(cls, user_id):
        expires_at = timezone.now() + datetime.timedelta(days=1)
        token_data = dict(user_id=user_id, expires_at=str(expires_at))
        token = cls.get_jwt_token(token_data)
        session_data = dict(user_id=user_id, expires_at=expires_at, token=token)
        return Session.objects.create(**session_data)


class UserService:

    @staticmethod
    def get_user(username):
        if not username:
            raise ValidationError("Please provide valid username")
        return User.objects.filter(username=username).first()

    @staticmethod
    def get_user_by_id(user_id):
        if not user_id:
            raise ValidationError("Please provide user")
        return User.objects.filter(id=user_id).first()

    @staticmethod
    def create_user(username, password):
        if not (username and password):
            raise ValidationError("Please provide valid username and password")
        # ideally we should encourage user for a strong password but for simplicity skipping that for now.
        return User.objects.create(username=username, password=password)

    @classmethod
    def login(cls, username, password):
        user = cls.get_user(username)
        if not user:
            raise ValidationError("User doesn't exist")
        # not hashing the password for simplicity, ideally it should be hashed and stored.
        if user.password != password:
            raise ValidationError("Invalid username password combination")
        user_id = user.id
        session = SessionService.get_active_session(user_id)
        if session:
            return session.token
        session = SessionService.create_session(user_id)
        return session.token

    @classmethod
    def signup(cls, username, password):
        user = cls.get_user(username)
        if user:
            raise ValidationError(f"User with {username} already exists")
        cls.create_user(username, password)
        return True

    @classmethod
    @auth_required
    def follow(cls, followed_id, **kwargs):
        user_id = kwargs['user_id']
        followed_user = cls.get_user_by_id(followed_id)
        if int(user_id) == int(followed_id):
            raise ValidationError(f"You cannot follow yourself")
        if not followed_user:
            raise ValidationError(f"User doesn't exist")
        Follow.objects.create(follower_id=user_id, followed_id=followed_id)


class PostService:

    @classmethod
    @auth_required
    def create_post(cls, text, **kwargs):
        user_id = kwargs['user_id']
        return Post.objects.create(user_id=user_id, text=text)

    @classmethod
    def get_post(cls, post_id):
        return Post.objects.filter(post_id=post_id).first()

    @classmethod
    def __update_score(cls, post_id):
        with transaction.atomic():
            Post.objects.filter(post_id=post_id).update(score=F('upvotes') - F('downvotes'))

    @classmethod
    @auth_required
    def upvote(cls, post_id, **kwargs):
        with transaction.atomic():
            Post.objects.filter(post_id=post_id).update(upvotes=F('upvotes') + 1)
            cls.__update_score(post_id)

    @classmethod
    @auth_required
    def downvote(cls, post_id, **kwargs):
        with transaction.atomic():
            Post.objects.filter(post_id=post_id).update(downvotes=F('downvotes') + 1)
            cls.__update_score(post_id)

    def __update_comment_count(self, post_id):
        with transaction.atomic():
            Post.objects.filter(post_id=post_id).update(comments_count=F('comments_count') + 1)


class CommentService:

    @classmethod
    @auth_required
    def create_comment(cls, post_id, text, parent_comment_id=None, **kwargs):
        user_id = kwargs['user_id']
        # avoiding validation of existence parent_comment_id for now for simplicity.
        Comment.objects.create(
            user_id=user_id, post_id=post_id, parent_comment_id=parent_comment_id, comment=text
        )
        ps = PostService()
        ps._PostService__update_comment_count(post_id)

    @classmethod
    @auth_required
    def upvote(cls, comment_id, **kwargs):
        with transaction.atomic():
            Comment.objects.filter(comment_id=comment_id).update(upvotes=F('upvotes') + 1)

    @classmethod
    @auth_required
    def downvote(cls, comment_id, **kwargs):
        with transaction.atomic():
            Comment.objects.filter(comment_id=comment_id).update(downvotes=F('downvotes') + 1)


class FeedService:

    sort_by_col_mapping = dict(score='score', comments='comments_count', timestamp='created_at')

    @classmethod
    @auth_required
    def get_feed(cls, **kwargs):
        user_id = kwargs['user_id']
        # sorting options values: score, comments, timestamp
        sort_by = kwargs.get('sort_by')
        sort_order = kwargs.get('sort_order') or 'desc'
        sort_order = sort_order.lower()
        followed_users = Follow.objects.filter(follower=user_id).values_list('followed', flat=True)
        posts = Post.objects.filter(user_id__in=followed_users)
        if not posts:
            return {}
        if sort_by:
            sort_col = cls.sort_by_col_mapping.get(sort_by)
            if sort_col:
                if sort_order == 'desc':
                    sort_col = f"-{sort_col}"
                posts = posts.order_by(sort_col)
        cols = ['user_id', 'text', 'upvotes', 'downvotes']
        return [p for p in posts.values(*cols)]
