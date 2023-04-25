from django.db import models
from django.utils import timezone

from insta.utils import display_time_in_cool_format


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    @classmethod
    def from_db(cls, db, field_names, values):
        instance = super(BaseModel, cls).from_db(db, field_names, values)
        instance._loaded_values = dict(zip(field_names, values))
        return instance


class User(BaseModel):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=20)

    @property
    def signed_up_at(self):
        now = timezone.now()
        return display_time_in_cool_format(self.created_at, now, postfix='ago')

    class Meta:
        indexes = [
            models.Index(fields=["username"], name="ix_user_username_123"),
        ]


class Session(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, to_field='id')
    token = models.CharField(max_length=255)
    expires_at = models.DateTimeField()

    @property
    def expires_at_str(self):
        now = timezone.now()
        if self.expires_at <= now:
            return "already expired"
        return display_time_in_cool_format(now, self.expires_at, prefix='in')

    class Meta:
        indexes = [
            models.Index(fields=["token"], name="ix_session_token_123"),
        ]


class Post(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, to_field='id')
    text = models.CharField(max_length=255)
    upvotes = models.IntegerField(default=0)
    downvotes = models.IntegerField(default=0)
    score = models.IntegerField(default=0)
    comments_count = models.IntegerField(default=0)

    @property
    def posted_at(self):
        now = timezone.now()
        return display_time_in_cool_format(self.created_at, now, postfix='ago')

    class Meta:
        indexes = [
            models.Index(fields=["score"], name="ix_post_score_123"),
            models.Index(fields=["comments_count"], name="ix_post_comments_count_123"),
        ]


class VotePostMap(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, to_field='id')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, to_field='id')
    vote = models.IntegerField()  # 0 means downvote, 1 means upvote


class Comment(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, to_field='id')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, to_field='id')
    parent_comment_id = models.CharField(max_length=255, null=True, blank=True)
    comment = models.CharField(max_length=255)
    upvotes = models.IntegerField(default=0)
    downvotes = models.IntegerField(default=0)

    @property
    def commented_at(self):
        now = timezone.now()
        return display_time_in_cool_format(self.created_at, now, postfix='ago')

    class Meta:
        indexes = [
            models.Index(fields=["post_id"], name="ix_comment_post_id_234"),
            models.Index(fields=["parent_comment_id"], name="ix_comment_pci_234"),
        ]


class VoteCommentMap(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, to_field='id')
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, to_field='id')
    vote = models.IntegerField()  # 0 means downvote, 1 means upvote


class Follow(BaseModel):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower', to_field='id')
    followed = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followed', to_field='id')

    @property
    def followed_at(self):
        now = timezone.now()
        return display_time_in_cool_format(self.created_at, now, postfix='ago')

    class Meta:
        unique_together = ('follower', 'followed')
