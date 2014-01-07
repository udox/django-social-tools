import twitter
from django.views.generic import TemplateView

class TweetUserView(TemplateView):
    template_name = 'tweet_user.html'

    def send_tweet(self):
        msg = self.request.GET['msg']
        target = self.request.GET['target']

        try:
            api = twitter.Api(
                consumer_key='aJsLPnXasjoWXW99cbG0lg',
                consumer_secret='DxW4hggyUqiwGhGfnzldX57BgBcx7RIpB8fBUDRoM',
                access_token_key='2272873393-Ig34VvEWmD4HN66bgNlZrRE7JfFmcndZvxzB116',
                access_token_secret='ZqMNHKhNQNLfikntnbP6MevM7I1aftHeBtBR0W2Rkibrx',
            )
            tweet = api.PostUpdate('@{!s} {!s}'.format(target, msg))
        except twitter.TwitterError:
            tweet = None
        return tweet

    def get_context_data(self, **kwargs):
        context = super(TweetUserView, self).get_context_data(**kwargs)
        context['tweet'] = self.send_tweet()

    def get(self, *args, **kwargs):
        return super(TweetUserView, self).get(*args, **kwargs)
