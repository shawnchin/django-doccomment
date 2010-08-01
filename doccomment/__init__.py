from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.utils.importlib import import_module

DEFAULT_PERMISSION_MODULE = 'doccomment.permissions'

def get_permission_class():
    """
    Returns class used to define permissions of users.
    
    Users can define their own class in settings.DOCCOMMENT_PERMISSION_MODULE. 
    This module must contain a class called Permission derived from
    doccomment.permissions.Permission
    
    Default: 'doccomment.permissions'
    """
    mod = getattr(settings, 'DOCCOMMENT_PERMISSION_MODULE', DEFAULT_PERMISSION_MODULE)
    try:
        permission_class = import_module(mod).Permission
    except ImportError:
        raise ImproperlyConfigured("The DOCCOMMENT_PERMISSION_MODULE (%r) "\
                                   "could not be imported" % settings.DOCCOMMENT_PERMISSION_MODULE)
    return permission_class