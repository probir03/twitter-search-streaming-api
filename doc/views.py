from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from collections import OrderedDict

@api_view(['GET'])
def get_doc(request):
	doc = OrderedDict()
	doc['create env'] = {
		'create' :"Create env.py File",
		"Add" : [
			"TWITTER_API_KEY = 'Twitter Consumer Kye'",
			"TWITTER_SECRET_KEY = 'Twitter Consumer Secret'",
			"TWITTER_ACCESS_TOKEN='Twitter Acccess Token'",
			"TWITTER_ACCESS_TOKEN_SECRET='Twitter Access Secret'",
			"DATABASE = 'postgresql'",
			"HOST = '127.0.0.1'",
			"DATABASE_NAME = 'databse_name'",
			"DATABASE_USERNAME = 'database_user'",
			"DATABASE_PASSWORD = 'database_password'"
		]
	}
	doc['run command'] = {
		'requierment' : 'pip install -r requierments.txt',
		'make migration' : 'pyhton manage.py makemigrations',
		'run migration' : 'pyhton manage.py migrate'
	}
	doc['stream track API'] = {
		'description' : 'This will add track and start fecthing data based on the track and store in database',
		'add track' : '/twitter/stream/tracks',
		'edit delete or update track' : '/twitter/stream/tracks/<id>'
	}
	doc['search_from_streamed_data'] = {
		'description' : 'first you have to add tracks then only results will come, This API will search from database which is store using twitter streaming api',
		'twitter search API' : 'twitter/stream',
		'params' : ['text', 'source', 'truncated', 'quote_count', 'reply_count', 'retweet_count', 'favorite_count', 'favorited',
  			'retweeted', 'hashtags', 'media', 'symbols', 'urls', 'user_mentions', 'extended_entities', 'created_at'
  		],
  		'operators' : ['__gt', '__icontains', '__lt', '__contains', '__isnull', '__gte', '__lte'],
  		'sort or order by' : [
  			'twitter/stream?text__icontains=car&quote_count__gt=10&sort=id.desc'
  			'twitter/stream?text__icontains=car&quote_count__gt=10&sort=id.asc,text.desc'
  		],
  		'examples' : [
  			'/twitter/stream?text__icontains=car&quote_count__gt=10',
  			'/twitter/stream?text__contains=car',
  			'/twitter/stream?quote_count__gt=10',
  			'/twitter/stream?reply_count__lt=100',
  		]
	}
	doc['twitter_search'] = {
		'description' : 'This API will search from the twitter using twitter search API, atleast one query have to pass to get result',
		'twitter stream search' : '/twitter/search?q=car',
		'params' : ['q', 'lang', 'locale', 'since_id', 'geocode',
			'max_id', 'since', 'until', 'result_type','count', 'include_entities', 'from',
	        'to', 'source'],
	    'examples' : [
	    	'/twitter/search?q=car&from=narendramodi',
  			'/twitter/search?q=car&lang=en',
	    ]
	}
	doc['export'] = {
		'description' : 'for now only csv export supported',
		'use' : 'add query paramet to the search url as export=csv',
		'example' : [
			'/twitter/search?q=car&from=narendramodi&export=csv',
  			'/twitter/stream?text__icontains=car&quote_count__gt=10&export=csv'
		]
	}

	return Response(doc)