from django.conf import settings
from django.conf.urls import patterns, include, url, static
from django.contrib import admin
from rest_framework import routers

from social.views import TweetUserView, BanUserView, PaginatedImagePostFeedView
from brand.views import MessageViewSet, MarketAccountViewSet


admin.autodiscover()
router = routers.DefaultRouter()
router.register(r'messages', MessageViewSet)
router.register(r'accounts', MarketAccountViewSet)

urlpatterns = patterns('',
    url(r'^', include(admin.site.urls)),
    url(r'^api/', include(router.urls)),
    url(r'^send-tweet/', TweetUserView.as_view(), name='tweet_user'),
    url(r'^ban-user/', BanUserView.as_view(), name='ban_user'),
    url(r'^api/image-feed/', PaginatedImagePostFeedView.as_view(), name='image_feed'),
) + static.static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
