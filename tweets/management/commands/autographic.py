# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand

from tweets.models import Tweet
from tweets.autographic import generator


class Command(BaseCommand):

    def __init__(self):
        super(Command, self).__init__()

    def handle(self, *args, **kwargs):
        """
            Import tweets from twitter for the first stored search term.
        """

        for tweet in Tweet.objects.exclude(deleted=True):
            generator(tweet)
            self.stdout.write("Generated Entry %d versions" % tweet.pk)
