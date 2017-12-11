from django.shortcuts import render
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream as twitt_stream
from django.conf import settings
import models, datetime, json
from rest_framework import generics
from serializers import StreamTrackSerializer
from rest_framework.response import Response
from django.shortcuts import redirect
from thread import start_new_thread

#Global dict
d = []
# twitter Oauth and get stream
def tweepy_auth():
	try :
		l = StdOutListener()
		tracks = []
		queryset = models.StreamTrack.objects.all()
		for d in queryset:
			tracks.append(d.label)
		auth = OAuthHandler(settings.TWITTER_API_KEY, settings.TWITTER_SECRET_KEY)
		auth.set_access_token(settings.TWITTER_ACCESS_TOKEN, settings.TWITTER_ACCESS_TOKEN_SECRET)
		stream = twitt_stream(auth, l)
		stream.filter(track=tracks)
		for i in d:
			i.disconnect()
		d = []
		d.append(stream)
	except Exception as e:
		pass

class StreamTrackCreateView(generics.ListCreateAPIView):
	"""docstring for StreamCreateView"""
	queryset = models.StreamTrack.objects.all()
	serializer_class = StreamTrackSerializer

	def post(self, request, *args, **kwargs):
		super(StreamTrackCreateView, self).post(request, *args, **kwargs)
		start_new_thread(tweepy_auth, ())
		return redirect('/twitter/stream/tracks')


class StreamTrackDetailsView(generics.RetrieveUpdateDestroyAPIView):
	"""This class handles the http GET, PUT and DELETE requests."""
	queryset = models.StreamTrack.objects.all()
	serializer_class = StreamTrackSerializer

	def delete(self, request, *args, **kwargs):
		super(StreamTrackDetailsView, self).delete(request, *args, **kwargs)
		start_new_thread(tweepy_auth, ())
		return redirect('/twitter/stream/tracks/'+args)

	def put(self, request, *args, **kwargs):
		super(StreamTrackDetailsView, self).put(request, *args, **kwargs)
		start_new_thread(tweepy_auth, ())
		return redirect('/twitter/stream/tracks/'+args)

#listener class
class StdOutListener(StreamListener):

	'''
	this method will call when response 200 from twitter api
	here data ar stored in database
	'''
	def on_data(self, data):
		data = json.loads(data)
		stream = models.Stream(
			id = str(data['id']),
			text = data['text'],
			source = data['source'],
			truncated = data['truncated'],
			quote_count = int(data['quote_count']),
			reply_count = int(data['reply_count']),
			retweet_count = int(data['retweet_count']),
			favorite_count = int(data['favorite_count']),
			favorited = bool(data['favorited']),
			retweeted = bool(data['retweeted']),
			hashtags = data['entities']['hashtags'],
			media = data['entities'].get('media'),
			symbols = data['entities']['symbols'],
			urls = data['entities']['urls'],
			user_mentions = data['entities']['user_mentions'],
			extended_entities = data.get('extended_entities'),
			created_at = datetime.datetime.strptime(data['created_at'],'%a %b %d %H:%M:%S +%f %Y'),
	    )
		stream.save()
		user = models.StreamUser(
	    	id = data['user']['id'],
			name = data['user']['name'],
			screen_name = data['user']['screen_name'],
			location = data['user']['location'],
			description = data['user']['description'],
			stream = stream,
			created_at=datetime.datetime.now()
	    )
		user.save()

	'''this method will call when twitter api throws error'''
	def on_error(self, status, *Args):
	    print status, "error", Args
