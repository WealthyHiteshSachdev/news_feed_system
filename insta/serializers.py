from rest_framework import serializers
from rest_framework.fields import SkipField
from rest_framework.relations import PKOnlyObject

from insta.models import Post, Comment


class ModifiedModelSerializer(serializers.ModelSerializer):

    def to_representation(self, instance):
        """
        Object instance -> Dict of primitive datatypes.
        """
        ret = {}
        fields = self._readable_fields

        for field in fields:
            try:
                attribute = field.get_attribute(instance)
            except SkipField:
                continue

            # We skip `to_representation` for `None` values so that fields do
            # not have to explicitly deal with that case.
            #
            # For related fields with `use_pk_only_optimization` we need to
            # resolve the pk value.
            check_for_none = attribute.pk if isinstance(attribute, PKOnlyObject) else attribute
            if check_for_none is None:
                ret[field.field_name] = None
            else:
                ret[field.field_name] = field.to_representation(attribute)

        return ret


class PostSerializer(ModifiedModelSerializer):
    comments = serializers.SerializerMethodField()
    username = serializers.SerializerMethodField()

    def get_comments(self, obj):
        comment_objs = Comment.objects.filter(post_id=obj.id, parent_comment_id__isnull=True)
        return CommentSerializer(comment_objs, many=True).data

    def get_username(self, obj):
        return obj.user.username

    class Meta:
        model = Post
        fields = ('id', 'username', 'text', 'upvotes', 'downvotes', 'score', 'comments_count', 'posted_at', 'comments')


class CommentSerializer(ModifiedModelSerializer):
    replies = serializers.SerializerMethodField()
    username = serializers.SerializerMethodField()

    def get_replies(self, obj):
        reply_objs = Comment.objects.filter(parent_comment_id=obj.id)
        return CommentSerializer(reply_objs, many=True).data

    def get_username(self, obj):
        return obj.user.username

    class Meta:
        model = Comment
        fields = ('id', 'username', 'comment', 'upvotes', 'downvotes', 'commented_at', 'replies')
