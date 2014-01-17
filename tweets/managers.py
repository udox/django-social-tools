from django.db import models
from django.db.models import Q


class TweetManager(models.Manager):

    def get_queryset(self):
        from models import MarketAccount, BannedUser

        accounts = MarketAccount.objects.all().values_list('handle', flat=True)
        banned_users = BannedUser.objects.all().values_list('handle', flat=True)

        account_min_date = '2014-01-13 00:00:00'

        return super(TweetManager, self).get_queryset().exclude(handle__in=accounts)\
            .exclude(deleted=True).exclude(content__contains='RT ').exclude(entry_allowed=False)\
            .exclude(handle__in=banned_users).filter(Q(user_joined__isnull=True)|Q(user_joined__lte=account_min_date))


class AllTweetManager(models.Manager):

    def get_queryset(self):
        return super(AllTweetManager, self).get_queryset()
