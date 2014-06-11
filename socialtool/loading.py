import sys
import traceback
from django.conf import settings
from django.db.models import get_model as django_get_model

from socialtool.exceptions import (ModuleNotFoundError, ClassNotFoundError,
                               AppNotFoundError)


def get_class(module_label, classname):
    """
Dynamically import a single class from the given module.

This is a simple wrapper around `get_classes` for the case of loading a
single class.

Args:
module_label (str): Module label comprising the app label and the
module name, separated by a dot. For example, 'catalogue.forms'.
classname (str): Name of the class to be imported.

Returns:
The requested class object or `None` if it can't be found
"""
    return get_classes(module_label, [classname])[0]


def get_classes(module_label, classnames):
    """
Dynamically import a list of classes from the given module.

This works by looping over ``INSTALLED_APPS`` and looking for a match
against the passed module label. If the requested class can't be found in
the matching module, then we attempt to import it from the corresponding
core socialtool app (assuming the matched module isn't in socialtool).

This is very similar to ``django.db.models.get_model`` function for
dynamically loading models. This function is more general though as it can
load any class from the matching app, not just a model.

Args:
module_label (str): Module label comprising the app label and the
module name, separated by a dot. For example, 'catalogue.forms'.
classname (str): Name of the class to be imported.

Returns:
The requested class object or ``None`` if it can't be found

Examples:

Load a single class:

>>> get_class('social.views', 'PaginatedImagePostFeedView')
socialtool.social.views.PaginatedImagePostFeedView

Load a list of classes:

>>> get_classes('social.views',
... ['PaginatedImagePostFeedView', 'BanUserView'])
[socialtool.social.views.PaginatedImagePostFeedView,
socialtool.social.views.BanUserView]

Raises:

AppNotFoundError: If no app is found in ``INSTALLED_APPS`` that matches
the passed module label.

ImportError: If the attempted import of a class raises an
``ImportError``, it is re-raised
"""
    if '.' not in module_label:
        # Importing from top-level modules is not supported, e.g.
        # get_class('shipping', 'Scale'). That should be easy to fix,
        # but @maikhoepfel had a stab and could not get it working reliably.
        # Overridable classes in a __init__.py might not be a good idea anyway.
        raise ValueError(
            "Importing from top-level modules is not supported")

    # import from socialtool package (should succeed in most cases)
    # e.g. 'socialtool.social.views'
    socialtool_module_label = "socialtool.%s" % module_label
    socialtool_module = _import_module(socialtool_module_label, classnames)

    # returns e.g. 'socialtool.social.views',
    # 'yourproject.apps.dashboard.catalogue' or 'dashboard.catalogue',
    # depending on what is set in INSTALLED_APPS
    installed_apps_entry, app_name = _find_installed_apps_entry(module_label)
    if installed_apps_entry.startswith('socialtool'):
        # The entry is obviously a socialtools one, we don't import again
        local_module = None
    else:
        # Attempt to import the classes from the local module
        # e.g. 'yourproject.dashboard.catalogue.forms'
        sub_module = module_label.replace(app_name, '')
        local_module_label = installed_apps_entry + sub_module
        local_module = _import_module(local_module_label, classnames)

    if socialtool_module is local_module is None:
        # This intentionally doesn't raise an ImportError, because ImportError
        # can get masked in complex circular import scenarios.
        raise ModuleNotFoundError(
            "The module with label '%s' could not be imported. This either"
            "means that it indeed does not exist, or you might have a problem"
            " with a circular import." % module_label
        )

    # return imported classes, giving preference to ones from the local package
    return _pluck_classes([local_module, socialtool_module], classnames)


def _import_module(module_label, classnames):
    """
Imports the module with the given name.
Returns None if the module doesn't exist, but propagates any import errors.
"""
    try:
        return __import__(module_label, fromlist=classnames)
    except ImportError:
        # There are 2 reasons why there could be an ImportError:
        #
        # 1. Module does not exist. In that case, we ignore the import and
        # return None
        # 2. Module exists but another ImportError occurred when trying to
        # import the module. In that case, it is important to propagate the
        # error.
        #
        # ImportError does not provide easy way to distinguish those two cases.
        # Fortunately, the traceback of the ImportError starts at __import__
        # statement. If the traceback has more than one frame, it means that
        # application was found and ImportError originates within the local app
        __, __, exc_traceback = sys.exc_info()
        frames = traceback.extract_tb(exc_traceback)
        if len(frames) > 1:
            raise


def _pluck_classes(modules, classnames):
    """
Gets a list of class names and a list of modules to pick from.
For each class name, will return the class from the first module that has a
matching class.
"""
    klasses = []
    for classname in classnames:
        klass = None
        for module in modules:
            if hasattr(module, classname):
                klass = getattr(module, classname)
                break
        if not klass:
            packages = [m.__name__ for m in modules if m is not None]
            raise ClassNotFoundError("No class '%s' found in %s" % (
                classname, ", ".join(packages)))
        klasses.append(klass)
    return klasses


def _get_installed_apps_entry(app_name):
    """
Given an app name (e.g. 'catalogue'), walk through INSTALLED_APPS
and return the first match, or None.
This does depend on the order of INSTALLED_APPS and will break if
e.g. 'dashboard.catalogue' comes before 'catalogue' in INSTALLED_APPS.
"""
    for installed_app in settings.INSTALLED_APPS:
        if installed_app.endswith(app_name):
            return installed_app
    return None


def _find_installed_apps_entry(module_label):
    """
Given a module label, finds the best matching INSTALLED_APPS entry.

This is made trickier by the fact that we don't know what part of the
module_label is part of the INSTALLED_APPS entry. So we try all possible
combinations, trying the longer versions first. E.g. for
'dashboard.catalogue.forms', 'dashboard.catalogue' is attempted before
'dashboard'
"""
    modules = module_label.split('.')
    # if module_label is 'dashboard.catalogue.forms.widgets', combinations
    # will be ['dashboard.catalogue.forms', 'dashboard.catalogue', 'dashboard']
    combinations = [
        '.'.join(modules[:-count]) for count in range(1, len(modules))]
    for app_name in combinations:
        entry = _get_installed_apps_entry(app_name)
        if entry:
            return entry, app_name
    raise AppNotFoundError(
        "Couldn't find an app to import %s from" % module_label)


def get_model(app_label, model_name, *args, **kwargs):
    """
Gets a model class by it's app label and model name. Fails loudly if the
model class can't be imported.
This is merely a thin wrapper around Django's get_model function.
"""
    model = django_get_model(app_label, model_name, *args, **kwargs)
    if model is None:
        raise ImportError(
            "{app_label}.{model_name} could not be imported.".format(
                app_label=app_label, model_name=model_name))
    return model
