from django.conf import settings
from django.conf.urls import patterns, include, url, static
from django.contrib import admin
from rest_framework import routers

from tweets.views import TweetUserView, MessageViewSet, MarketAccountViewSet, AssignArtworkerView

admin.autodiscover()
router = routers.DefaultRouter()
router.register(r'messages', MessageViewSet)
router.register(r'accounts', MarketAccountViewSet)

urlpatterns = patterns('',
    url(r'^', include(admin.site.urls)),
    url(r'^api/', include(router.urls)),
    url(r'^send-tweet/', TweetUserView.as_view(), name='tweet_user'),
    url(r'^assign-artworker/', AssignArtworkerView.as_view(), name='assign_artworker'),
) + static.static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
