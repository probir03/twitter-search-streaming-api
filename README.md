# twitter-search-streaming-api
 Create env.py file
 	```sh
 	$ touch env.py
 	```
 Create new app in twitter and get the credential
 	- url : https://apps.twitter.com/
 	
 Add env data 
 	- TWITTER_API_KEY = 'Twitter Consumer Kye'
 	- TWITTER_SECRET_KEY = 'Twitter Consumer Secret'
 	- TWITTER_ACCESS_TOKEN='Twitter Acccess Token'
 	- TWITTER_ACCESS_TOKEN_SECRET='Twitter Access Secret'
 	- DATABASE = 'postgresql'
 	- HOST = '127.0.0.1'
 	- DATABASE_NAME = 'databse_name'
 	- DATABASE_USERNAME = 'database_user'
 	- DATABASE_PASSWORD = 'database_password'

Run in console for installation
	```sh
	$ pip install -r requirements.txt
	$ python manage.py migrate
	$ python manage.py runserver
	```

Open browser and hit
	- http://127.0.0.1:8000/doc/
	- you can see all the api documentation

