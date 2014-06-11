import twitter
import urllib
from datetime import datetime

from django.db.utils import IntegrityError
from django.http import HttpResponse
from django.views.generic import TemplateView, View
from rest_framework import generics, viewsets

from socialtool.loading import get_classes, get_model


PostSerializer, PaginatedPostSerializer, MessageSerializer, \
MarketAccountSerializer = get_classes('social.serializers', ('PostSerializer', 'PaginatedPostSerializer', 'MessageSerializer', 'MarketAccountSerializer'))

HasImageFilterBackend, OldSchoolRetweet = get_classes('social.filters', ('HasImageFilterBackend', 'OldSchoolRetweet'))

# TODO - tweet and artworker assignments should be returning a JSON
# response - although having said that we are just swapping out HTML
# for returned HTML - so maybe not! ~jaymz


class TweetUserView(TemplateView):
    template_name = 'tweet_user.html'

    def send_tweet(self):
        tweet_pk = self.request.GET['tweet_pk']
        msg = self.request.GET['msg']

        tweet = get_model('social', 'socialpost').objects.get(pk=tweet_pk)

        # Reverse the quoting and get the unicode back
        msg = urllib.unquote(msg)

        try:
            api = twitter.Api(
                consumer_key=tweet.account.consumer_key,
                consumer_secret=tweet.account.consumer_secret,
                access_token_key=tweet.account.access_token_key,
                access_token_secret=tweet.account.access_token_secret,
            )

            # If we have an included media file then attach and send that
            # otherwise we post a regular Update instead - that is we're
            # not going by the message content!
            if tweet.photoshop:
                status = api.PostMedia(u'{!s}'.format(msg), tweet.photoshop.file.name,
                    in_reply_to_status_id=tweet.uid)
            else:
                status = api.PostUpdate(u'{!s}'.format(msg), in_reply_to_status_id=tweet.uid)

            # Update the tweet itself now
            tweet.tweeted = True
            tweet.tweet_id = status.id
            tweet.sent_tweet = msg
            tweet.tweeted_by = self.request.user
            tweet.tweeted_at = datetime.now()
            tweet.save()

        except twitter.TwitterError:
            status = None

        return status

    def get_context_data(self, **kwargs):
        context = super(TweetUserView, self).get_context_data(**kwargs)
        context['tweet'] = self.send_tweet()
        return context

    def get(self, *args, **kwargs):
        return super(TweetUserView, self).get(*args, **kwargs)


class BanUserView(View):
    template_name = 'assign_artworker.html'

    def ban_user(self):
        post_pk = self.request.GET['post_pk']

        tweet = get_model('social', 'socialpost').everything.get(pk=post_pk)
        hellban = get_model('social', 'banneduser')(handle=tweet.handle)

        try:
            hellban.save()
        except IntegrityError:
            return "Already banned"

        return "OK"

    def get(self, request, *args, **kwargs):
        return HttpResponse(self.ban_user())


class PaginatedImagePostFeedView(generics.ListAPIView):
    queryset = get_model('social', 'socialpost').objects.all()
    serializer_class = PostSerializer
    pagination_serializer_class = PaginatedPostSerializer
    filter_backends = (HasImageFilterBackend, OldSchoolRetweet)

    def get_queryset(self):
        queryset = get_model('social', 'socialpost').objects.all()
        user = self.request.QUERY_PARAMS.get('user', None)
        if user is not None:
            try:
                # If we have a user then we need to look up what accounts they are associated
                # with and then filter on all those (it's M2M)
                tracked_term = get_model('social', 'trackedterms').objects.get(user__username=user)
                queryset = queryset.filter(search_term__in=tracked_term.terms.values_list('pk', flat=True))
            except get_model('social', 'trackedterms').DoesNotExist:
                # If we can't find the user just carry on
                pass
        return queryset


class MessageViewSet(viewsets.ModelViewSet):
    queryset = get_model('social', 'message').objects.all()
    serializer_class = MessageSerializer
    filter_fields = ('type', 'account',)


class MarketAccountViewSet(viewsets.ModelViewSet):
    queryset = get_model('social', 'marketaccount').objects.all()
    serializer_class = MarketAccountSerializer
