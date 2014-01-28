from django.contrib.admin import SimpleListFilter
from django.db.models import Q


class SocialPostImageFilter(SimpleListFilter):
    title = 'image source'
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


class SocialPostStatusFilter(SimpleListFilter):
    title = 'Post status'
    parameter_name = 'messaged'

    def lookups(self, request, model_admin):
        return (
            ('yes', 'Messaged'),
            ('no', 'Not Messaged yet'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'yes':
            return queryset.filter(messaged=True)

        if self.value() == 'no':
            return queryset.filter(messaged=False)

        return queryset
