# -*- coding: utf-8 -*-

from optparse import make_option

from django.conf import settings
from django.core.management.base import BaseCommand

from tweets.models import Tweet


class Command(BaseCommand):

    option_list = BaseCommand.option_list + (
        make_option('--all',
            action='store_true',
            dest='all',
            default=False,
            help='Show all status, including ok tweets'),
        )

    def __init__(self):
        super(Command, self).__init__()

    def delete(self, tweet, reason='Unknown'):
        tweet.deleted = True
        tweet.entry_allowed = False
        tweet.disallowed_reason = reason
        tweet.save()

    def handle(self, *args, **kwargs):
        """
            Check if we need to hide some historic tweets
        """

        cnt = 0
        for tweet in Tweet.objects.exclude(deleted=True):
            cnt += 1

            if cnt % 100 == 0:
                self.stdout.write('Processed %d so far' % cnt)

            if tweet.image_url is None:
                self.delete(tweet, reason='No image supplied')
                self.stdout.write('%d has no image' % tweet.id)

            # Check if we need to disable this for having an existing graphic -
            # this will set explictly
            if tweet.has_existing_graphic:
                self.delete(tweet, reason='Has existing graphic')
                self.stdout.write('%d has a graphic already' % tweet.id)
                continue

            # Ok, now see how many times they've entered this since this tweet,
            # if it's more than the max we'll ignore them
            preexisting_entries = Tweet.everything.filter(handle=tweet.handle, created_at__lte=tweet.created_at).count()
            if preexisting_entries > settings.MAX_ENTRIES:
                self.delete(tweet, reason='Already entered max times (%d)' % preexisting_entries)
                self.stdout.write('%d - %s already entered %d times' % (tweet.id, tweet.handle, preexisting_entries))
                continue

            if kwargs['all']:
                self.stdout.write("%d %s is ok" % (tweet.id, tweet.handle))
