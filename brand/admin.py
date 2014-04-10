from django.contrib import admin

from models import Message, MarketAccount, TrackedTerms
from social.admin import BaseAdmin


class MessageAdmin(BaseAdmin):
    list_display = ('account', 'type', 'copy')
    list_filter = ('account', 'type')

admin.site.register(Message, MessageAdmin)
admin.site.register(MarketAccount, BaseAdmin)
admin.site.register(TrackedTerms, BaseAdmin)
