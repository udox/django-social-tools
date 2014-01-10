from django.contrib.admin import SimpleListFilter
from django.db.models import Q


class TwitterImageFilter(SimpleListFilter):
    title = 'Image source'
    parameter_name = 'image_url'

    def lookups(self, request, model_admin):
        return (
            ('any', 'Twitpic or Twitter'),
            ('twitpic', 'Twitpic only'),
            ('twitter', 'Twitter only'),
            ('none', 'No image'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'twitter':
            return queryset.filter(image_url__icontains='pbs.twimg.com')

        if self.value() == 'twitpic':
            return queryset.filter(image_url__icontains='twitpic.com')

        if self.value() == 'any':
            return queryset.filter(Q(image_url__icontains='twitpic.com')|Q(image_url__icontains='pbs.twimg.com'))

        if self.value() == 'none':
            return queryset.filter(image_url=None)

        return queryset


class TweetStatusFilter(SimpleListFilter):
    title = 'Tweet status'
    parameter_name = 'tweeted'

    def lookups(self, request, model_admin):
        return (
            ('yes', 'Tweeted'),
            ('no', 'Not tweeted yet'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'yes':
            return queryset.filter(tweeted=True)

        if self.value() == 'no':
            return queryset.filter(tweeted=False)

        return queryset
