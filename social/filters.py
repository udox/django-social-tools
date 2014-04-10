from rest_framework import filters

from django.contrib.admin import SimpleListFilter
from django.db.models import Q


class SocialPostImageFilter(SimpleListFilter):
    title = 'image source'
    parameter_name = 'image_url'

    def lookups(self, request, model_admin):
        return (
            ('any', 'All images'),
            ('twitpic', 'Twitpic only'),
            ('twitter', 'Twitter only'),
            ('instagram', 'Instagram only'),
            ('none', 'No image'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'twitter':
            return queryset.filter(image_url__icontains='pbs.twimg.com')

        if self.value() == 'twitpic':
            return queryset.filter(image_url__icontains='twitpic.com')

        if self.value() == 'instagram':
            return queryset.filter(image_url__icontains='distilleryimage')

        if self.value() == 'any':
            return queryset.filter(
                Q(image_url__icontains='twitpic.com')|\
                Q(image_url__icontains='pbs.twimg.com')|\
                Q(image_url__icontains='distilleryimage')
            )

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


class HasImageFilterBackend(filters.BaseFilterBackend):
    """
        Filter for API to exclude posts without images
    """

    def filter_queryset(self, request, queryset, view):
        return queryset.exclude(image_url=None)


class OldSchoolRetweet(filters.BaseFilterBackend):
    """
        Filter for API to exclude posts that start "@handle... which is
        like an old school retweet hence the name. \u021c is the left
        double quote mark.

        (http://www.fileformat.info/info/unicode/char/201C/index.htm)
    """

    def filter_queryset(self, request, queryset, view):
        return queryset.exclude(content__regex=r'[\u201c|"]@')
