# -*- coding: utf-8 -*-
import twitter
import sys
from dateutil.parser import parse as date_parse

from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError

from tweets.models import Tweet, SearchTerm, MarketAccount


class Command(BaseCommand):

    def __init__(self):
        super(Command, self).__init__()
        self.accounts = MarketAccount.objects.all()
        self.primary_account = MarketAccount.objects.get(handle='adidasoriginals')

    def get_api(self):
        """
            Get a twitter api object to work with
        """

        return twitter.Api(
            consumer_key='aJsLPnXasjoWXW99cbG0lg',
            consumer_secret='DxW4hggyUqiwGhGfnzldX57BgBcx7RIpB8fBUDRoM',
            access_token_key='2272873393-Ig34VvEWmD4HN66bgNlZrRE7JfFmcndZvxzB116',
            access_token_secret='ZqMNHKhNQNLfikntnbP6MevM7I1aftHeBtBR0W2Rkibrx',
        )

    def get_image_url(self, tweet):
        """
            Try and extract an image url from a tweet - our preference is for
            the offical twitter attached entity, failing that look for twitpic
        """

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

        return image_url

    def get_account(self, tweet):
        """
            Check for the presence of a tracked account in the tweet. If nothing
            can be found we default to a particular one.
        """
        for account in self.accounts:
            if account.handle in tweet.text:
                return account

        return self.primary_account


    def handle(self, *args, **kwargs):
        """
            Import tweets from twitter for the first stored search term.
        """

        terms = SearchTerm.objects.filter(active=True)

        for term in terms:

            self.stdout.write("\nImporting %s tweets" % term.term)

            api = self.get_api()
            search = api.GetSearch(term=term.term, result_type='recent', count=100)

            for tweet in search:

                obj = Tweet(
                    created_at=date_parse(tweet.created_at),
                    uid=tweet.id,
                    handle=tweet.user.screen_name,
                    account=self.get_account(tweet),
                    image_url=self.get_image_url(tweet),
                    content=tweet.text,
                    followers=tweet.user.followers_count,
                )

                try:
                    obj.save()
                    self.stdout.write("Added %s (%d)" % (obj.uid, obj.id))
                except IntegrityError:
                    self.stdout.write("Tweet already exists %s" % obj.uid)
