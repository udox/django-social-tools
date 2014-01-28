from django.contrib import admin
from django.utils.safestring import mark_safe
from models import SocialPost, SearchTerm, BannedUser
from filters import SocialPostImageFilter, SocialPostStatusFilter

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


class SocialAdmin(BaseAdmin):
    search_fields = ('handle', 'content',)
    list_display = ('created_at', 'high_priority', 'get_handle', 'account', 'get_image', 'content', 'messages', 'messaged_by', 'get_artworker', 'notes')
    list_filter = ('account', 'high_priority', SocialPostStatusFilter, SocialPostImageFilter, 'artworker', 'messaged_by', 'created_at', 'messaged_at', 'entry_allowed')
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
        ('Tweet data', {
            'classes': ('collapse', ),
            'fields': ('created_at', 'handle', 'user_joined', 'account', 'content', 'image_url', 'uid', 'entry_allowed', 'disallowed_reason'),
        }),
        ('Sent data', {
            'classes': ('collapse', ),
            'fields': ('artworker', 'messaged_by', 'messaged_at', 'tweet_id', 'sent_tweet', )
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
                <li><a class="btn btn-inverse ban-user">Ban User</a></li>
                <!--<li><a class="btn btn-danger send-tweet" data-msgtype="tryagain">Image doesn't work</a></li>-->
                <!--<li><a class="btn btn-success send-tweet" data-msgtype="imagelink">Tweet tongue graphic</a></li>-->
            </ul>
        """)
    messages.short_description = 'Tweet back to user'

    def get_artworker(self, obj):
        if obj.artworker:
            return obj.artworker.username
        else:
            return mark_safe("""
                <a class="btn btn-info assign-artworker">Start Working!</a>
            """)
    get_artworker.short_description = 'Artworker Status'

    def save_model(self, request, obj, form, change):
        # TODO: fix bug with this - if a CM edits and saves a tweet directly
        # this will set the artworker to them
        if 'photoshop' in form.changed_data:
            obj.artworker = request.user

        obj.save()

    def get_actions(self, request):
        actions = super(SocialAdmin, self).get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def get_queryset(self, request):
        if request.user.is_superuser:
            return self.model.everything.get_query_set()

        return super(SocialAdmin, self).get_queryset(request)

admin.site.register(SocialPost, SocialAdmin)
admin.site.register(SearchTerm, BaseAdmin)
admin.site.register(BannedUser, BaseAdmin)
