from django.db import models


class TweetManager(models.Manager):

    def get_queryset(self):
        from models import MarketAccount

        accounts = MarketAccount.objects.all().values_list('handle', flat=True)
        return super(TweetManager, self).get_queryset().exclude(handle__in=accounts).exclude(deleted=True)
