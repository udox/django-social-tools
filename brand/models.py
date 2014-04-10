from django.db import models
from django.contrib.auth.models import User


class MarketAccount(models.Model):
    """
        This model allows us to actual query the social networks and interact
        with them.
    """
    ACCOUNT_CHOICES = (
        ('twitter', 'Twitter'),
        ('instagram', 'Instagram'),
    )

    type = models.CharField(max_length=50, unique=True, choices=ACCOUNT_CHOICES)
    handle = models.CharField(max_length=100)
    active = models.BooleanField(default=True)

    # Optionally associate with a particular user for filtering/ACL
    user = models.ForeignKey(User, blank=True, null=True)

    # Instagram
    client_id = models.CharField(max_length=100, blank=True, null=True)
    client_secret = models.CharField(max_length=100, blank=True, null=True)

    # Twitter
    consumer_secret = models.CharField(max_length=100, blank=True, null=True)
    consumer_key = models.CharField(max_length=100, blank=True, null=True)
    access_token_secret = models.CharField(max_length=100, blank=True, null=True)
    access_token_key = models.CharField(max_length=100, blank=True, null=True)

    def __unicode__(self):
        return u'{0} ({1})'.format(self.handle, self.type)


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


class TrackedTerms(models.Model):
    """
        Associate a particular user with various search terms. We can then
        filter on these to give a particular feed
    """
    user = models.ForeignKey(User, unique=True)
    terms = models.ManyToManyField('social.SearchTerm')

    def __unicode__(self):
        return u'{} ({})'.format(self.user, ','.join(self.terms.values_list('term', flat=True)))

    class Meta:
        verbose_name_plural = 'Tracked Terms'
