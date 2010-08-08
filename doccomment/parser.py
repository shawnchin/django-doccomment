from markdown import markdown
from BeautifulSoup import BeautifulSoup, Tag
from django.conf import settings

DEFAULT_EXTENSIONS = []
DEFAULT_SAFEMODE   = True

def parse(text):
    """
    Parses input text and returns HTML. Use markdown by default.
    
    This routine may be overridden to allow different input formats.
    """
    md_extensions = getattr(settings, "DOCCOMMENT_MARKDOWN_EXTENSIONS", DEFAULT_EXTENSIONS)
    md_safemode   = getattr(settings, "DOCCOMMENT_MARKDOWN_SAFEMODE", DEFAULT_SAFEMODE)
    return markdown(text, md_extensions, safe_mode=md_safemode)

def input_to_html(text):
    """
    Parses input text and returns HTML as tuple of (html, block_list),
    where "html" is the complete HTML document, and block_list the same
    HTML document split up into a list of top-level blocks.
    
    Use parser.parse() to convert text to HTML. The default routine
    users Markdown.
    
    BeautifulSoup is used to sanitise generated HTML
    """
    
    soup = BeautifulSoup(parse(text))
    html = unicode(soup.prettify())
    block_list = [e.__unicode__() for e in soup.contents if type(e) == Tag]
    
    return (html, block_list)

    