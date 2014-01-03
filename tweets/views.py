import twitter
from django.views.generic import TemplateView

class TweetUserView(TemplateView):
    template_name = 'tweet_user.html'

    def get(self, *args, **kwargs):

        api = twitter.Api(
            consumer_key='aJsLPnXasjoWXW99cbG0lg',
            consumer_secret='DxW4hggyUqiwGhGfnzldX57BgBcx7RIpB8fBUDRoM',
            access_token_key='2272873393-Ig34VvEWmD4HN66bgNlZrRE7JfFmcndZvxzB116',
            access_token_secret='ZqMNHKhNQNLfikntnbP6MevM7I1aftHeBtBR0W2Rkibrx',
        )

        try:
            api.PostUpdate('Hello! Test')
        except twitter.TwitterError:
            pass

        return super(TweetUserView, self).get(*args, **kwargs)
