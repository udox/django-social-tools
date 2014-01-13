from django.db import models
from django.contrib.auth.models import User
from managers import TweetManager


class MarketAccount(models.Model):
    handle = models.CharField(max_length=100)
    consumer_secret = models.CharField(max_length=100)
    consumer_key = models.CharField(max_length=100)
    access_token_secret = models.CharField(max_length=100)
    access_token_key = models.CharField(max_length=100)

    def __unicode__(self):
        return u'{0} ({1})'.format(self.handle, self.pk)


class Message(models.Model):
    MESSAGE_TYPES = (
        ('f', 'Fail'),
        ('s', 'Success'),
    )

    copy = models.CharField(max_length=140)
    account = models.ForeignKey(MarketAccount)
    type = models.CharField(max_length=1, choices=MESSAGE_TYPES)

    def __unicode__(self):
        return u'{0} ({1}...)'.format(self.account, self.copy[:30])


class Tweet(models.Model):
    created_at = models.DateTimeField()
    created_at.verbose_name = 'Tweet Date'
    uid = models.CharField(max_length=100, unique=True)
    handle = models.CharField(max_length=100)
    followers = models.IntegerField(blank=True, null=True)
    content = models.CharField(max_length=150)
    content.verbose_name = 'User\'s Tweet'
    image_url = models.URLField(max_length=255, blank=True, null=True)
    tweeted = models.BooleanField(default=False)
    tweeted.verbose_name = 'Tweet status'
    approved = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)
    photoshop = models.ImageField(upload_to='uploads', blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    notes.verbose_name = 'Internal Notes'
    account = models.ForeignKey(MarketAccount, blank=True, null=True)
    account.verbose_name = 'Adidas\' Handle'
    sent_tweet = models.CharField(max_length=140, blank=True, null=True)
    artworker = models.ForeignKey(User, related_name='artworker', blank=True, null=True)
    tweeted_by = models.ForeignKey(User, related_name='tweeter', blank=True, null=True)
    tweeted_at = models.DateTimeField(blank=True, null=True)
    tweet_id = models.CharField(max_length=100, blank=True, null=True)

    def __unicode__(self):
        return u'{0} - {1} ({2})'.format(self.handle, self.account, self.tweeted)

    class Meta:
        # Tweets should be in ascending date order
        ordering = ('created_at', 'handle',)

    # Exclude all deleted tweets - we keep them in so they aren't reimported
    # or added elsewhere
    objects = TweetManager()


class SearchTerm(models.Model):
    active = models.BooleanField(default=False)
    term = models.CharField(max_length=100)

    def __unicode__(self):
        return u'{0} ({1})'.format(self.term, self.active)
