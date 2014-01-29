# -*- coding: utf-8 -*-

import pickle

from optparse import make_option

from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError
from django.conf import settings

from social.models import SocialPost, SearchTerm
from social.facades import SocialSearchFacade
from brand.models import MarketAccount


class Command(BaseCommand):

    option_list = BaseCommand.option_list + (
        make_option(
            '-c', '--count', action='store', dest='post_count', type='int',
            help='Posts to import per network', default=10,
        ),
    )

    def __init__(self):
        super(Command, self).__init__()
        self.accounts = MarketAccount.objects.all()

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

                self.stdout.write("\nImporting %s posts on %s for account %s" % (term.term, account.type, account.handle))

                api = SocialSearchFacade(account)
                search = api.search(term.term, count=kwargs.get('post_count'))

                for post in search:

                    obj = SocialPost(
                        account=account,
                        content=post.content,
                        created_at=post.created_at,
                        followers=post.followers,
                        handle=post.handle,
                        image_url=post.image_url,
                        post_url=post.post_url,
                        uid=post.uid,
                        user_joined=post.user_joined,
                        profile_image=post.profile_image,
                        raw_object=pickle.dumps(post._obj),
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
