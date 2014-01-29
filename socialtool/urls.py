from django.conf import settings
from django.conf.urls import patterns, include, url, static
from django.contrib import admin
from rest_framework import routers

from social.views import TweetUserView, BanUserView, ImagePostFeedViewSet, AllPostFeedViewSet
from brand.views import MessageViewSet, MarketAccountViewSet


admin.autodiscover()
router = routers.DefaultRouter()
router.register(r'messages', MessageViewSet)
router.register(r'accounts', MarketAccountViewSet)
router.register(r'image-feed', ImagePostFeedViewSet)
router.register(r'post-feed', AllPostFeedViewSet)

urlpatterns = patterns('',
    url(r'^', include(admin.site.urls)),
    url(r'^api/', include(router.urls)),
    url(r'^send-tweet/', TweetUserView.as_view(), name='tweet_user'),
    url(r'^ban-user/', BanUserView.as_view(), name='ban_user'),
) + static.static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
