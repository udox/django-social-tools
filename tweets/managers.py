from django.db import models


class TweetManager(models.Manager):

    def get_queryset(self):
        return super(TweetManager, self).get_queryset().exclude(deleted=True)
