from django.contrib import admin
from django.utils.safestring import mark_safe
from tweets.models import Tweet, Photoshop

# Register your models here.

class TweetAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'handle', 'country', 'image', 'complete', 'tweeted')
    list_filter = ('country', 'tweeted')

    def image(self, obj):
        return mark_safe('<img src="%s" width=100 />' % obj.image_url)

    def complete(self, obj):
        return obj.photoshop is not None


admin.site.register(Tweet, TweetAdmin)
admin.site.register(Photoshop)
