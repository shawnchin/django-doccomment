from markdown import markdown
from BeautifulSoup import BeautifulSoup, Tag
from django.conf import settings

DEFAULT_EXTENSIONS = []
DEFAULT_SAFEMODE   = True
DEFAULT_DIV_ID_PREFIX = "DE-"

def parse(text):
    """
    Parses input text and returns HTML. Use markdown by default.
    
    This routine may be overridden to allow different input formats.
    """
    md_extensions = getattr(settings, "DOCCOMMENT_MARKDOWN_EXTENSIONS", DEFAULT_EXTENSIONS)
    md_safemode   = getattr(settings, "DOCCOMMENT_MARKDOWN_SAFEMODE", DEFAULT_SAFEMODE)
    return markdown(text, md_extensions, safe_mode=md_safemode)

def parse_elements(text):
    """
    Parses input text and returns a list of HTML blocks which makes
    up the whole document,
    
    Uses parser.parse() to convert text to HTML. The default routine
    users Markdown.
    
    BeautifulSoup is used to sanitise generated HTML, and split it up
    into top-level blocks.
    
    Each element is wrapped with a DIV with and ID so it can be easily
    targetted by JS/CSS. The DIVs have IDs in the form "DE-<N>" where 
    <N> is the sequence number starting from 0. The prefix ("DE-")
    can be modified using settings.DOCCOMMENT_DIV_ID_PREFIX
    """
    
    # get id prefix
    id_prefix = getattr(settings, "DOCCOMMENT_DIV_ID_PREFIX", DEFAULT_DIV_ID_PREFIX)
   
    # sanitise and split using BeautifulSoup
    soup = BeautifulSoup(parse(text))
    elements = [e for e in soup.contents if type(e) == Tag]
    
    # wrap blocks in <div>
    format = u"<div id='%s%d'>\n%s\n</div>"
    for seq,txt in enumerate(elements):
        elements[seq] = format % (id_prefix, seq, txt)
    
    return elements

    