# -*- coding: utf-8 -*-
import twitter
import os
import requests
import subprocess
from dateutil.parser import parse as date_parse

from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError
from django.core.files import File

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

        source = None

        try:
            source, image_url = 'twitter', tweet.media[0]['media_url']

        except IndexError:
            try:
                expanded_url = tweet.urls[0].expanded_url

                if 'twitpic' in expanded_url or 'pbs.twimg.com' in expanded_url:
                    source, image_url = 'twitpic', tweet.urls[0].expanded_url
                else:
                    image_url = None

            except IndexError:
                image_url = None

        return source, image_url

    def get_account(self, tweet):
        """
            Check for the presence of a tracked account in the tweet. If nothing
            can be found we default to a particular one.
        """
        for account in self.accounts:
            if account.handle.lower() in tweet.text.lower():
                return account

        return self.primary_account

    def autographic(self, tweet):
        """
            Generate an automatic version using imagemagick that may be suitable
            to ease artworker load. Also create a blank base with the handle and
            a fully composed one which may be tweeted back.
        """
        url = tweet.image_url
        tmp_file = os.path.join('/tmp', os.path.basename(url))
        with open(tmp_file, 'wb') as img:
            img.write(requests.get(url).content)

        stan_process = subprocess.Popen(['tweets/scripts/stanify.sh', tmp_file, tweet.handle], stdout=subprocess.PIPE)
        out, err = stan_process.communicate()

        output = out.strip()

        auto_file = os.path.join('/tmp/', 'stan.%s' % output)
        composed_file = os.path.join('/tmp/', 'composed.stan.%s' % output)
        base_file = os.path.join('/tmp/', 'base.stan.%s' % output)

        tweet.auto_photoshop.save(os.path.basename(auto_file), File(open(auto_file)))
        tweet.auto_compose.save(os.path.basename(composed_file), File(open(composed_file)))
        tweet.auto_base.save(os.path.basename(base_file), File(open(base_file)))

        return

    def first_entry(self, tweet):
        """
            Check if this user has already entered
        """
        return Tweet.objects.filter(handle=tweet.user.screen_name).count() == 0

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

                source, image_url = self.get_image_url(tweet)

                obj = Tweet(
                    created_at=date_parse(tweet.created_at),
                    uid=tweet.id,
                    handle=tweet.user.screen_name,
                    account=self.get_account(tweet),
                    image_url=image_url,
                    content=tweet.text,
                    followers=tweet.user.followers_count,
                    first_entry=self.first_entry(tweet),
                )

                try:
                    obj.save()
                    self.stdout.write("Added %s (%d)" % (obj.uid, obj.id))

                    if source == 'twitter':
                        self.autographic(obj)

                except IntegrityError:
                    self.stdout.write("Tweet already exists %s" % obj.uid)
