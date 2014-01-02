import twitter
from tweets.models import SearchTerm

api = twitter.Api(
    consumer_key='aJsLPnXasjoWXW99cbG0lg',
    consumer_secret='DxW4hggyUqiwGhGfnzldX57BgBcx7RIpB8fBUDRoM',
    access_token_key='2272873393-Ig34VvEWmD4HN66bgNlZrRE7JfFmcndZvxzB116',
    access_token_secret='ZqMNHKhNQNLfikntnbP6MevM7I1aftHeBtBR0W2Rkibrx',
)

search = api.GetSearch(term=SearchTerm.objects.get(active=True).term)
for tweet in search:
    print tweet.media
