from django.contrib import admin
from django.utils.safestring import mark_safe
from tweets.models import Tweet, SearchTerm

# Register your models here.

def mark_deleted(modeladmin, request, queryset):
    queryset.update(deleted=True)
mark_deleted.short_description = 'Mark selected tweets as deleted'

def mark_approved(modeladmin, request, queryset):
    queryset.update(approved=True)
mark_approved.short_description = 'Mark selected tweets as approved'


class TweetAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'get_handle', 'country', 'get_image', 'get_photoshop', 'content', 'approved',
        'messages', 'tweeted', 'notes')
    list_filter = ('country', 'approved', 'tweeted')
    list_editable = ('approved', 'notes')
    search_fields = ('handle', 'content',)
    actions = [mark_deleted, mark_approved]

    def get_image(self, obj):
        return mark_safe('<a href="{0}" target="_blank"><img src="{0}" width=100 /></a>'.format(obj.image_url))

    def get_handle(self, obj):
        return mark_safe('<a href="http://twitter.com/{0}" target="_blank">{0}</a>'.format(obj.handle.encode('utf-8')))

    def messages(self, obj):
        return mark_safe("""
            <ul class="message-btns">
                <li><a class="btn btn-danger send_tweet" data-msgtype="tryagain">Try Again</a></li>
                <li><a class="btn btn-success send_tweet" data-msgtype="imagelink">Image Link</a></li>
            </ul>
        """)

    def get_photoshop(self, obj):
        if obj.photoshop:
            return mark_safe('<a href="{0}" target="_blank"><img src={0} width=100 /></a>'.format(obj.photoshop.url))
        else:
            return mark_safe('<a class="btn btn-warning" ref="/admin/tweets/tweet/{}">Upload</a>'.format(obj.id))

    class Media:
        js = ('js/tweet_admin.js', )
        css = {
            'all': ('css/adi051.css', )
        }


admin.site.register(Tweet, TweetAdmin)
admin.site.register(SearchTerm)
