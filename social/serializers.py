from rest_framework import serializers
from rest_framework import pagination
from social.models import SocialPost, Message, MarketAccount


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


class MessageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Message


class MarketAccountSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = MarketAccount
