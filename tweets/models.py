from django.db import models
from django_countries import CountryField

from managers import TweetManager


class Photoshop(models.Model):
    created_at = models.DateTimeField(auto_now=True, auto_now_add=True)
    image = models.ImageField(upload_to='uploads')

    def __unicode__(self):
        return self.image


class Tweet(models.Model):
    created_at = models.DateTimeField()
    uid = models.CharField(max_length=100, unique=True)
    handle = models.CharField(max_length=100)
    content = models.CharField(max_length=150)
    image_url = models.URLField(max_length=255, blank=True, null=True)
    photoshop = models.OneToOneField(Photoshop, blank=True, null=True)
    tweeted = models.BooleanField(default=False)
    approved = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)
    country = CountryField()

    def __unicode__(self):
        return '%s - %s (%s)' % (self.handle, self.country, self.tweeted)

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
        return '%s (%s)' % (self.term, self.active)
