from rest_framework import serializers
from models import SocialPost


class PostSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = SocialPost
        fields = ('image_url', 'post_url', 'handle', 'content', 'post_source')
