from django.conf import settings
from django.conf.urls import patterns, include, url, static
from django.contrib import admin

from tweets.views import TweetUserView

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^send-tweet/', TweetUserView.as_view(), name='tweet_user'),
) + static.static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

