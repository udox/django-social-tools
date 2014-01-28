# -*- coding: utf-8 -*-

from dateutil.parser import parse as date_parse

from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError
from django.conf import settings

from social.models import SocialPost, SearchTerm
from social.facades import SocialSearchFacade
from brand.models import MarketAccount


class Command(BaseCommand):

    def __init__(self):
        super(Command, self).__init__()
        self.accounts = MarketAccount.objects.all()

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

    def disable(self, post, reason='Unknown'):
        post.deleted = True
        post.entry_allowed = False
        post.disallowed_reason = reason
        post.save()

    def handle(self, *args, **kwargs):
        """
            Import for the first stored search term.
        """

        terms = SearchTerm.objects.filter(active=True)

        for term in terms:

            for account in self.accounts:

                self.stdout.write("\nImporting %s posts for account %s" % (term.term, account.handle))

                api = SocialSearchFacade(account)
                search = api.search(term.term)

                for post in search:

                    source, image_url = self.get_image_url(post)

                    obj = SocialPost(
                        created_at=date_parse(post.created_at),
                        uid=post.id,
                        handle=post.user.screen_name,
                        account=account,
                        image_url=image_url,
                        content=post.text,
                        followers=post.user.followers_count,
                        user_joined=date_parse(post.user.created_at),
                    )

                    try:
                        obj.save()
                        self.stdout.write("Added %s (%d %s)" % (obj.uid, obj.id, obj.handle))

                        entry_count = obj.entry_count
                        if entry_count > settings.MAX_ENTRIES:
                            self.disable(obj, reason='Already entered max times (%d)' % entry_count)
                            continue

                    except IntegrityError:
                        self.stdout.write("Post already exists %s (%s)" % (obj.uid, obj.handle))
