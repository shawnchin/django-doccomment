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


DEFAULT_PARSER_MODULE = 'doccomment.parser'
def get_parser_module():
    """
    Returns module that should contain the parse() function to parse 
    document text to HTML.
    
    Users can define their own class in settings.DOCCOMMENT_PARSER_MODULE. 
    This module must contain a function called parse(text) which returns
    and HTML string.
    """
    mod = getattr(settings, 'DOCCOMMENT_PARSER_MODULE', DEFAULT_PARSER_MODULE)
    try:
        parser_module = import_module(mod)
    except ImportError:
        raise ImproperlyConfigured("The DOCCOMMENT_PARSER_MODULE (%r) "\
                                   "could not be imported" % settings.DOCCOMMENT_PARSER_MODULE)
    return parser_module