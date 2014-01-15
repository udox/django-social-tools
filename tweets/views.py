import twitter
import urllib
from datetime import datetime
from django.views.generic import TemplateView
from rest_framework import viewsets
from models import Message, MarketAccount, Tweet
from serializers import MessageSerializer, MarketAccountSerializer


# TODO - tweet and artworker assignments should be returning a JSON
# response - although having said that we are just swapping out HTML
# for returned HTML - so maybe not! ~jaymz


class TweetUserView(TemplateView):
    template_name = 'tweet_user.html'

    def send_tweet(self):
        tweet_pk = self.request.GET['tweet_pk']
        msg = self.request.GET['msg']

        tweet = Tweet.objects.get(pk=tweet_pk)

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


class AssignArtworkerView(TemplateView):
    template_name = 'assign_artworker.html'

    def assign_artworker(self):
        tweet_pk = self.request.GET['tweet_pk']
        tweet = Tweet.objects.get(pk=tweet_pk)

        if tweet.artworker is None:
            tweet.artworker = self.request.user
            tweet.save()
            return True
        else:
            return tweet.artworker.username

    def get_context_data(self, **kwargs):
        context = super(AssignArtworkerView, self).get_context_data(**kwargs)
        context['artworker'] = self.assign_artworker()
        return context

    def get(self, *args, **kwargs):
        return super(AssignArtworkerView, self).get(*args, **kwargs)


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    filter_fields = ('type', 'account',)


class MarketAccountViewSet(viewsets.ModelViewSet):
    queryset = MarketAccount.objects.all()
    serializer_class = MarketAccountSerializer
