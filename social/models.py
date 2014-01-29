from django.db import models
from django.contrib.auth.models import User
from managers import SocialPostManager, AllSocialPostManager
from brand.models import MarketAccount


class BannedUser(models.Model):
    handle = models.CharField(max_length=100, unique=True)
    reason = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.handle


class SearchTerm(models.Model):
    active = models.BooleanField(default=False)
    term = models.CharField(max_length=100)

    def __unicode__(self):
        return u'{0} ({1})'.format(self.term, self.active)


class SocialPost(models.Model):
    created_at = models.DateTimeField()
    created_at.verbose_name = 'Post date'
    uid = models.CharField(max_length=100, unique=True)
    post_url = models.URLField(max_length=255, null=True, blank=True)
    handle = models.CharField(max_length=100)
    followers = models.IntegerField(blank=True, null=True)
    user_joined = models.DateTimeField(blank=True, null=True)
    profile_image = models.URLField(max_length=255, blank=True, null=True)
    content = models.CharField(max_length=500)
    approved = models.BooleanField(default=False)
    high_priority = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)
    entry_allowed = models.BooleanField(default=True)
    notes = models.TextField(blank=True, null=True)
    notes.verbose_name = 'internal notes'
    account = models.ForeignKey(MarketAccount, blank=True, null=True)
    account.verbose_name = 'Social source'
    content.verbose_name = 'user\'s post'
    image_url = models.URLField(max_length=255, blank=True, null=True)
    messaged = models.BooleanField(default=False)
    messaged.verbose_name = 'Post status'
    sent_message = models.CharField(max_length=140, blank=True, null=True)
    # note the FKs: https://docs.djangoproject.com/en/dev/topics/db/models/#be-careful-with-related-name
    messaged_by = models.ForeignKey(User, related_name='%(class)s_messenger', blank=True, null=True)
    messaged_at = models.DateTimeField(blank=True, null=True)
    sent_id = models.CharField(max_length=100, blank=True, null=True)
    disallowed_reason = models.TextField(blank=True, null=True)

    raw_object = models.TextField(blank=True, null=True)
    raw_object.help_text = 'Pickled string version of the complete API returned content'

    # Exclude all deleted tweets - we keep them in so they aren't reimported
    # or added elsewhere
    objects = SocialPostManager()
    everything = AllSocialPostManager()

    def __unicode__(self):
        return u'{0} - {1} ({2})'.format(self.handle, self.account.type, self.messaged)

    class Meta:
        # Content should be in ascending date order
        ordering = ('-high_priority', '-created_at', '-followers', 'handle')

    @property
    def entry_count(self):
        """
            Return how many times this handle has entered - we're only counting
            when they tweeted with an image - otherwise we'll exclude just tagged
            tweets - this isn't perfect - they might tweet something else and
            attach an image but should be ok
        """
        return SocialPost.everything.filter(handle=self.handle).exclude(image_url=None).exclude(uid=self.uid).count()
