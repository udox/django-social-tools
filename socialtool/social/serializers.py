from rest_framework import serializers
from rest_framework import pagination
from socialtool.loading import get_model


class PostSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = get_model('social', 'socialpost')
        fields = ('image_url', 'post_url', 'handle', 'content', 'post_source', 'created_at')


class PaginatedPostSerializer(pagination.PaginationSerializer):
    """
    Serializes page objects of user querysets.
    """
    class Meta:
        object_serializer_class = PostSerializer


class MessageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = get_model('social', 'message')


class MarketAccountSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = get_model('social', 'marketaccount')
