===================
Django-social-tools
===================

Django-social-tools is a Django app that scrapes social posts from instagram and twitter based on search terms
that can be configured through the admin screen.


Quick start
-----------

1. Add "social" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = (
        ...
        'polls',
    )

2. Include the social URLconf in your project urls.py like this::

    url(r'^social/', include('social.urls')),

3. Run `python manage.py migrate` to create the social models.

4. Run `python manage.py sync` to import social posts. This should be running
in a cron job to ensure data is fresh
