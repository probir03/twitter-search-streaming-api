# -*- coding: utf-8 -*-
# api/views.py
from django.conf import settings
from django.shortcuts import render, HttpResponse
from rest_framework import generics, views
from rest_framework import serializers
from rest_framework.response import Response
import requests, base64, oauth2, json
from stream.serializers import StreamSerializer
from stream import models
from tweepy import OAuthHandler
import tweepy, urllib, csv, uuid, datetime
from pagination import StandardResultsSetPagination
import json

COUNT = 100

"""
get the tweepy api object
"""
def api_obj(key=settings.TWITTER_ACCESS_TOKEN, secret=settings.TWITTER_ACCESS_TOKEN_SECRET, http_method="GET", post_body="", http_headers=None):
	auth = OAuthHandler(settings.TWITTER_API_KEY, settings.TWITTER_SECRET_KEY)
	auth.set_access_token(settings.TWITTER_ACCESS_TOKEN, settings.TWITTER_ACCESS_TOKEN_SECRET)
	return tweepy.API(auth)

"""
buld query for twitter search apis 
"""
def build_query_params(query):
	"""
	query_params = ['q', 'lang', 'locale', 'since_id', 'geocode',
	                       'max_id', 'since', 'until', 'result_type',
	                       'count', 'include_entities', 'from',
	                       'to', 'source']
	"""
	params = {}
	if 'q' in query:
		params['q'] = query['q']
	if 'lang' in query:
		params['lang'] = query['lang']
	if 'locale' in query:
		params['locale'] = query['locale']
	if 'lang' in query:
		params['lang'] = query['lang']
	if 'since_id' in query:
		params['since_id'] = query['since_id']
	if 'geocode' in query:
		params['geocode'] = query['geocode']
	if 'max_id' in query:
		params['max_id'] = query['max_id']
	if 'since' in query:
		params['since'] = query['since']
	if 'until' in query:
		params['until'] = query['until']
	if 'result_type' in query:
		params['result_type'] = query['result_type']
	if 'count' in query:
		params['count'] = query['count']
	else:
		params['count'] = COUNT
	if 'include_entities' in query:
		params['include_entities'] = query['include_entities']
	if 'from' in query:
		params['from'] = query['from']
	if 'to' in query:
		params['to'] = query['to']
	if 'source' in query:
		params['source'] = query['source']
	return params

"""
export to csv the twitter search data
"""
def export_search_to_csv(wr, response):
    wr.writerow(['text', 'source', 'truncated', 'retweet_count', 'favorite_count', 'favorited',
			'retweeted', 'created_at', 'user'])
    for rep in response:
    	wr.writerow([rep['text'].encode('utf-8').strip(), rep['source'].encode('utf-8').strip(), rep['truncated'],
	    	rep['retweet_count'], rep['favorite_count'], rep['favorited'],
  			rep['retweeted'], rep['created_at'],rep['user']['name'].encode('utf-8').strip()
			])

"""
get user name ofa twitt
"""
def get_user(data):
	if isinstance(data.get('user'), list):
		return None
	if isinstance(data.get('user'), dict):
		return data.get('user').get('name').encode('utf-8').strip()
	return None

"""
export the stream fetched data to database
"""
def export_stream_to_csv(wr, response):
    wr.writerow(['text', 'source', 'truncated', 'retweet_count', 'favorite_count', 'favorited',
			'retweeted', 'created_at', 'user'])
    for rep in response:
    	print rep, rep.get('user')
    	wr.writerow([rep['text'].encode('utf-8').strip(), rep['source'].encode('utf-8').strip(), rep['truncated'],
	    	rep['retweet_count'], rep['favorite_count'], rep['favorited'],
  			rep.get('retweeted'), rep.get('created_at'),get_user(rep)
			])

"""
Filter the stream saved data in database
"""
class FilterStreamView(generics.ListAPIView):
    """This class defines the create behavior of our rest api."""
    serializer_class = StreamSerializer
    pagination_class = StandardResultsSetPagination
    queryset = models.Stream.objects.all()

    def get_queryset(self):
    	if hasattr(self, 'filter_data'):
    		return models.Stream.objects.filter(**self.filter_data).all()
    	if hasattr(self, 'sort_data'):
    		self.queryset = self.queryset.order_by(*self.sort_data)
    	return self.queryset.all()
    
    """
	 query_params = [text, source, truncated, quote_count, reply_count, retweet_count, favorite_count, favorited,
  	retweeted, hashtags, media, symbols, urls, user_mentions, extended_entities, created_at]
  	"""
    def get(self, request, *args, **kwargs):
    	if len(request.query_params) <= 0:
    		return super(FilterStreamView, self).get(request, *args, **kwargs)
    	if len(request.query_params) > 0:
    		self.filter_data = {}
    		self.sort_data = []
    		for key, value in request.query_params.iteritems():
    			if key not in ['page', 'items', 'export', 'group', 'sort']:
    				self.filter_data[key] = request.query_params.get(key)
    			elif key == 'sort':
    				data = value.split(',')
    				for d in data:
    					pair = d.split('.')
    					if len(pair) > 1 and pair[1] == 'desc':
    						self.sort_data.append('-'+pair[0])
    					else :
    						self.sort_data.append(pair[0])
		try :
			if 'export' in request.query_params:
				res = HttpResponse(content_type='text/csv')
				res['Content-Disposition'] = 'attachment; filename="export_filter.csv"'
				writer = csv.writer(res)
				export_stream_to_csv(writer, self.get_serializer(self.get_queryset(), many=True).data)
				return res
			return super(FilterStreamView, self).get(request, *args, **kwargs)
		except Exception as e:
			return Response(e.message)


"""
Filter on twitter search apis
"""
class FilterTwitterSearchView(views.APIView):
	"""docstring for FilterTwitterSearchView"""

	def get(self, request):
		try :
			api = api_obj()
			params = build_query_params(request.query_params)
			data = api.search(**params)
			response = []
			for d in data:
				response.append(d.__dict__['_json'])
			if 'export' in request.query_params:
				res = HttpResponse(content_type='text/csv')
				res['Content-Disposition'] = 'attachment; filename="export_filter.csv"'
				writer = csv.writer(res)
				export_search_to_csv(writer, response)
				return res
			return Response(response)
		except : 
			return Response("No record Found or atleast give on Query parameters")
		
