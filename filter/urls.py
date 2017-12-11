# api/urls.py

from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from .views import FilterStreamView, FilterTwitterSearchView
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    url(r'^twitter/stream$', FilterStreamView.as_view(), name="stream"),
    url(r'^twitter/search$', FilterTwitterSearchView.as_view(), name="search"),
]

urlpatterns = format_suffix_patterns(urlpatterns)