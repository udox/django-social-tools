from django.contrib import admin
from django.utils.safestring import mark_safe
from models import Tweet, SearchTerm, Message, MarketAccount
from filters import TwitterImageFilter, TweetStatusFilter, TongueGraphicFilter

# Register your models here.

def mark_deleted(modeladmin, request, queryset):
    queryset.update(deleted=True)
mark_deleted.short_description = 'Hide selected tweets'

def mark_approved(modeladmin, request, queryset):
    queryset.update(approved=True)
mark_approved.short_description = 'Mark selected tweets as approved'


class BaseAdmin(admin.ModelAdmin):

    class Media:
        js = ('js/tweet_admin.js', )
        css = {
            'all': ('css/adi051.css', )
        }


class MessageAdmin(BaseAdmin):
    list_display = ('account', 'type', 'copy')
    list_filter = ('account', 'type')


class TweetAdmin(BaseAdmin):
    search_fields = ('handle', 'content',)
    list_display = ('created_at', 'high_priority', 'get_handle', 'account', 'get_image', 'get_autophotoshop', 'get_photoshop', 'content', 'messages', 'tweeted_by', 'get_artworker', 'notes')
    list_filter = ('account', 'high_priority', TweetStatusFilter, TwitterImageFilter, TongueGraphicFilter, 'artworker', 'tweeted_by', 'created_at', 'tweeted_at', 'entry_allowed')
    list_editable = ('notes', )

    list_per_page = 25

    actions = [mark_deleted, ]

    fieldsets = (
        ('Attach your photoshop', {
            'fields': ('photoshop', ),
        }),
        ('Make high priority', {
            'fields': ('high_priority', 'notes'),
        }),
        ('View/change autophotoshop', {
            'classes': ('collapse', ),
            'fields': ('auto_base', ('auto_photoshop_1', 'auto_compose_1'), ('auto_photoshop_2', 'auto_compose_2'), ('auto_photoshop_3', 'auto_compose_3')),
        }),
        ('Tweet data', {
            'classes': ('collapse', ),
            'fields': ('created_at', 'handle', 'account', 'content', 'image_url', 'uid', 'entry_allowed', 'disallowed_reason'),
        }),
        ('Sent data', {
            'classes': ('collapse', ),
            'fields': ('artworker', 'tweeted_by', 'tweeted_at', 'tweet_id', 'sent_tweet', )
        }),
    )

    def get_image(self, obj):
        if obj.image_url:
            if 'twitpic' in obj.image_url:
                url = 'http://twitpic.com/show/thumb/{}'.format(obj.image_url.split('/')[-1])
            else:
                url = obj.image_url

            return mark_safe('<a href="{0}" target="_blank"><img src="{1}" width=100 /></a>'.format(obj.image_url, url))
        else:
            return "N/A"
    get_image.short_description = 'Original Image'

    def get_handle(self, obj):
        return mark_safe("""
            <p><a href="http://twitter.com/{0}" target="_blank">{0}</a></p>
            <p><em>({1} Followers)
        """.format(obj.handle.encode('utf-8'), obj.followers))
    get_handle.short_description = 'User\'s Handle'

    def messages(self, obj):
        return mark_safe("""
            <ul class="message-btns">
                <li><a class="btn btn-danger send_tweet" data-msgtype="tryagain">Image doesn't work</a></li>
                <li><a class="btn btn-success send_tweet" data-msgtype="imagelink">Tweet tongue graphic</a></li>
            </ul>
        """)
    messages.short_description = 'Tweet back to user'

    def get_photoshop(self, obj):
        if obj.photoshop:
            if obj.tweet_id:
                # Open up the actual tweet if it's been sent
                return mark_safe('<a href="http://twitter.com/{0}/status/{2}" target="_blank"><img src={1} width=100 /></a>'.\
                    format(obj.account.handle, obj.photoshop.url, obj.tweet_id))
            else:
                # Otherwise direct to the local image
                return mark_safe('<a href="{0}" target="_blank"><img src={0} width=100 /></a>'.format(obj.photoshop.url))
        else:
            return mark_safe('<a class="btn btn-warning" href="/tweets/tweet/{}">Upload</a>'.format(obj.id))
    get_photoshop.short_description = 'Tongue Graphic'

    def get_autophotoshop(self, obj):
        auto, base, composed = ["N/A", ] * 3, "N/A", ["N/A", ] * 3

        if obj.auto_base:
            base = '<a class="autoshop" href="{0}" target="_blank"><img src={0} /></a><br>'.format(obj.auto_base.url)

        num_of_files = 3
        files = range(1, num_of_files + 1)
        for cnt in files:

            if getattr(obj, 'auto_photoshop_%d' % cnt):
                auto[cnt - 1] = '<a class="autoshop" href="{0}" target="_blank"><img src={0} /></a>'.format(getattr(obj, 'auto_photoshop_%d' % cnt).url)

            if getattr(obj, 'auto_compose_%d' % cnt):
                composed[cnt - 1] = '<a class="autoshop" href="{0}" target="_blank"><img src={0} /></a>'.format(getattr(obj, 'auto_compose_%d' % cnt).url)

        args  = [base, ] + auto + composed

        return mark_safe("""
            <table class="autogen-results">
                <tr><td colspan="3" align="center" class="base-img">%s</td></tr>
                <tr><td>%s</td><td>%s</td><td>%s</td></tr>
                <tr><td>%s</td><td>%s</td><td>%s</td></tr>
            </table>
        """ % (args[0], args[1], args[2], args[3], args[4], args[5], args[6]))

    get_autophotoshop.short_description = 'Automatic Graphic'

    def get_artworker(self, obj):
        if obj.artworker:
            return obj.artworker.username
        else:
            return mark_safe("""
                <a class="btn btn-info assign-artworker">Start Working!</a>
            """)
    get_autophotoshop.short_description = 'Artworker Status'

    def save_model(self, request, obj, form, change):
        # TODO: fix bug with this - if a CM edits and saves a tweet directly
        # this will set the artworker to them
        if 'photoshop' in form.changed_data:
            obj.artworker = request.user

        obj.save()

    def get_actions(self, request):
        actions = super(TweetAdmin, self).get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions


admin.site.register(Tweet, TweetAdmin)
admin.site.register(SearchTerm, BaseAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(MarketAccount, BaseAdmin)
