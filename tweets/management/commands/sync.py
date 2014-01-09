# -*- coding: utf-8 -*-
import twitter
import sys
from dateutil.parser import parse as date_parse

from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError

from tweets.models import Tweet, SearchTerm


class Command(BaseCommand):


    def handle(self, *args, **kwargs):
        """
            Import tweets from twitter for the first stored search term.
        """

        api = twitter.Api(
            consumer_key='aJsLPnXasjoWXW99cbG0lg',
            consumer_secret='DxW4hggyUqiwGhGfnzldX57BgBcx7RIpB8fBUDRoM',
            access_token_key='2272873393-Ig34VvEWmD4HN66bgNlZrRE7JfFmcndZvxzB116',
            access_token_secret='ZqMNHKhNQNLfikntnbP6MevM7I1aftHeBtBR0W2Rkibrx',
        )

        terms = SearchTerm.objects.filter(active=True)

        for term in terms:

            self.stdout.write("\nImporting %s tweets" % term.term)
            search = api.GetSearch(term=term.term)

            for tweet in search:
                try:
                    image_url = tweet.media[0]['media_url']

                except IndexError:
                    try:
                        expanded_url = tweet.urls[0].expanded_url

                        if 'twitpic' in expanded_url:
                            image_url = tweet.urls[0].expanded_url
                        else:
                            image_url = None

                    except IndexError:
                        image_url = None

                obj = Tweet(
                    created_at=date_parse(tweet.created_at),
                    uid=tweet.id,
                    handle=tweet.user.screen_name,
                    account=None,
                    image_url=image_url,
                    content=tweet.text,
                )
                try:
                    obj.save()
                    self.stdout.write("Added %s (%d)" % (obj.uid, obj.id))
                except IntegrityError:
                    self.stdout.write("Tweet already exists %s" % obj.uid)
