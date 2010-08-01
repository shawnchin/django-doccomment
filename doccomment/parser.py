from markdown import markdown
from django.conf import settings

DEFAULT_EXTENSIONS = []
DEFAULT_SAFEMODE   = True

def parse(text):
    """
    Parses input text and returns HTML. Use markdown by default.
    """
    md_extensions = getattr(settings, "DOCCOMMENT_MARKDOWN_EXTENSIONS", DEFAULT_EXTENSIONS)
    md_safemode   = getattr(settings, "DOCCOMMENT_MARKDOWN_SAFEMODE", DEFAULT_SAFEMODE)
    return markdown(text, md_extensions, safe_mode=md_safemode)