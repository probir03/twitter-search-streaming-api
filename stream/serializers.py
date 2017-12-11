from rest_framework import serializers
from .models import Stream, StreamUser, StreamTrack
import json

class StreamUserSerializer(serializers.ModelSerializer):
    """Serializer to map the Model instance into JSON format."""
    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = StreamUser
        fields = ('name', 'screen_name', 'location')

class StreamSerializer(serializers.ModelSerializer):
    """Serializer to map the Model instance into JSON format."""

    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = Stream
        fields = ('id', 'text', 'source', 'truncated', 'quote_count', 'reply_count', 'retweet_count',
			'favorite_count','favorited','retweeted','hashtags','media','symbols','urls', 'user_mentions',
			'extended_entities','created_at', 'user'
		)

class StreamTrackSerializer(serializers.ModelSerializer):
    """Serializer to map the Model instance into JSON format."""
    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = StreamTrack
        fields = ('id', 'label')