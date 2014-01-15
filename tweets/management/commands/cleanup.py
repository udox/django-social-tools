# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand
from tweets.models import Tweet


class Command(BaseCommand):

    def __init__(self):
        super(Command, self).__init__()

    def handle(self, *args, **kwargs):
        """
            Check if we need to hide some historic tweets
        """

        for tweet in Tweet.objects.exclude(deleted=True):
            pass
