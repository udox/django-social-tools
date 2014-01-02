from django.contrib import admin
from django.utils.safestring import mark_safe
from tweets.models import Tweet, Photoshop, SearchTerm

# Register your models here.

class TweetAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'get_handle', 'country', 'get_image', 'content', 'complete', 'tweeted')
    list_filter = ('country', 'tweeted')

    def get_image(self, obj):
        return mark_safe('<a href="{0}" target="_blank"><img src="{0}" width=100 /></a>'.format(obj.image_url))

    def get_handle(self, obj):
        return mark_safe('<a href="http://twitter.com/{0}" target="_blank">{0}</a>'.format(obj.handle.encode('utf-8')))

    def complete(self, obj):
        return obj.photoshop is not None


admin.site.register(Tweet, TweetAdmin)
admin.site.register(Photoshop)
admin.site.register(SearchTerm)
