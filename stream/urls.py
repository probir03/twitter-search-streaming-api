# api/urls.py

from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
import views 
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = {
	url(r'^twitter/stream/tracks$', views.StreamTrackCreateView.as_view(), name="add_stream"),
	url(r'^twitter/stream/tracks/(?P<pk>[0-9]+)/$', views.StreamTrackDetailsView.as_view(), name="update_stream"),
}

urlpatterns = format_suffix_patterns(urlpatterns)