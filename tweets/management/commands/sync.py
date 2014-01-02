# -*- coding: utf-8 -*-
import twitter
import sys

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

        try:
            term = SearchTerm.objects.filter(active=True)[0].term
        except (SearchTerm.DoesNotExist, IndexError):
            self.stdout.write('ERROR! Please add an active search term to the admin')
            sys.exit(1)

        search = api.GetSearch(term=term)

        for tweet in search:
            if len(tweet.media) == 1:
                obj = Tweet(
                    created_at=tweet.created_at,
                    uid=tweet.id,
                    handle=tweet.user.screen_name,
                    country='GB',
                    image_url=tweet.media[0]['media_url'],
                    content=tweet.text,
                )
                try:
                    obj.save()
                    self.stdout.write("Added %s (%d)" % (obj.uid, obj.id))
                except IntegrityError:
                    self.stdout.write("Tweet already exists %s" % obj.uid)
