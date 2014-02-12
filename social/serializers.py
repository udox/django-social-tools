from rest_framework import serializers
from rest_framework import pagination
from models import SocialPost


class PostSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = SocialPost
        fields = ('image_url', 'post_url', 'handle', 'content', 'post_source', 'created_at')


class PaginatedPostSerializer(pagination.PaginationSerializer):
    """
    Serializes page objects of user querysets.
    """
    class Meta:
        object_serializer_class = PostSerializer

