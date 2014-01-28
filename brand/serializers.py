from rest_framework import serializers
from models import Message, MarketAccount


class MessageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Message


class MarketAccountSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = MarketAccount
