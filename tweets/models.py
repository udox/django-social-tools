from django.db import models
from django_countries import CountryField


class Photoshop(models.Model):
    created_at = models.DateTimeField(auto_now=True, auto_now_add=True)
    image = models.ImageField(upload_to='uploads')

    def __unicode__(self):
        return self.image


class Tweet(models.Model):
    created_at = models.DateTimeField(auto_now=True, auto_now_add=True)
    uid = models.CharField(max_length=100, unique=True)
    handle = models.CharField(max_length=100)
    content = models.CharField(max_length=150)
    image_url = models.URLField(max_length=255, blank=True, null=True)
    photoshop = models.OneToOneField(Photoshop, blank=True, null=True)
    country = CountryField()
    tweeted = models.BooleanField(default=False)

    def __unicode__(self):
        return '%s - %s (%s)' % (self.handle, self.country, self.tweeted)

    class Meta:
        # Tweets should be in ascending date order
        ordering = ('created_at', 'handle',)


class SearchTerm(models.Model):
    active = models.BooleanField(default=False)
    term = models.CharField(max_length=100)

    def __unicode__(self):
        return '%s (%s)' % (self.term, self.active)
