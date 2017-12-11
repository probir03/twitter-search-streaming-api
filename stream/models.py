from django.contrib.postgres.fields import JSONField
from django.db import models
# import views

class StreamTrack(models.Model):
	"""docstring for StreamTracks"""
	label = models.CharField(max_length=100)	

	class Meta:
		db_table = 'stream_tracks'	

class Stream(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    text = models.TextField(null=True)
    source = models.TextField(null=True)
    truncated = models.TextField(null=True)
    quote_count = models.IntegerField(null=True)
    reply_count = models.IntegerField(null=True)
    retweet_count = models.IntegerField(null=True)
    favorite_count = models.IntegerField(null=True)
    favorited = models.BooleanField(default=0)
    retweeted = models.BooleanField(default=0)
    hashtags = models.TextField(null=True)
    media = models.TextField(null=True)
    symbols = models.TextField(null=True)
    urls = models.TextField(null=True)
    user_mentions = models.TextField(null=True)
    extended_entities = JSONField(null=True)
    created_at = models.DateTimeField(null=False)

    class Meta :
    	db_table = 'streams'

   
class StreamUser(models.Model):
 	"""docString for Stream_user"""
	id = models.CharField(max_length=255, primary_key=True)
	name = models.CharField(max_length=255, null=True)
	screen_name = models.CharField(max_length=255, null=True)
	location = models.CharField(max_length=255, null=True)
	description = models.TextField(null=True)
	stream = models.ForeignKey(Stream, on_delete=models.CASCADE, related_name='user')
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta :
		db_table = 'stream_users'


