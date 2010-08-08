from django.db import models
from django.contrib.auth.models import User
from django.contrib.comments.models import Comment
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import slugify

from managers import DocumentManager

class Document(models.Model):
    """
    A simple document model
    """
    NOT_PUBLISHED = _("(not published)")
    
    title  = models.CharField(_("title"), max_length=200)
    slug   = models.SlugField(editable=False, max_length=40)
    author = models.ForeignKey(User)
    body   = models.TextField(_("document text"))
    published = models.BooleanField(_("published"), default=False)
    date_created = models.DateTimeField(_("date_created"), auto_now_add=True)
    date_updated = models.DateTimeField(_("date_updated"), auto_now=True)
    date_published = models.DateTimeField(_("date_published"), blank=True, null=True)
    latest_version = models.CharField(_("latest_version"), max_length=15, default=NOT_PUBLISHED)
    has_modification = models.BooleanField(
        _("has modification"),
        default=True, 
        help_text=_("Modified since last publication?")
    )
   
    objects = DocumentManager()
    
    class Meta:
        verbose_name = _("document")
        verbose_name_plural = _("documents")
        ordering = ("-date_published",)
    
    def _get_html(self):
        from doccomment import get_parser_module
        return get_parser_module().parse(self.body)
    html = property(_get_html)
    
    def _get_possible_next_versions(self):
        ver = self.latest_version.split(".")
        if self.latest_version == Document.NOT_PUBLISHED or len(ver) != 3:
            major, minor, revision = (0,0,0)
        else:
            major = int(ver[0])
            minor = int(ver[1])
            revision = int(ver[2])
        
        opt = [
            [major,   minor,   revision+1],
            [major,   minor+1, 0         ],
            [major+1, 0,       0         ],
        ]
        out = ["%d.%d.%d"%(x,y,z) for x,y,z in opt]
        return out
    next_version_choices = property(_get_possible_next_versions)
    
    def save(self):
        self.slug = slugify(self.title)[:40]
        super(Document, self).save()

    def __unicode__(self):
        return self.title
        


class DocumentVersion(models.Model):
    """
    A published version of the document
    """
    document = models.ForeignKey(Document)
    title    = models.CharField(_("title"), max_length=200) # Snapshot of the title
    author   = models.ForeignKey(User)
    body     = models.TextField(_("document text")) # Snapshot of document
    rendered = models.TextField(_("rendered document"))
    elem_count = models.IntegerField(_("number of elements in page"))
    version_string = models.CharField(_("version string"), db_index=True, max_length=15)
    date_published = models.DateTimeField(_("date_published"), auto_now_add=True)
    
    class Meta:
        verbose_name = _("document version")
        verbose_name_plural = _("document versions")
        ordering = ('document', '-date_published',)
        
    def __unicode__(self):
        return "%s (v%s)" % (self.document, self.version_string)
        
        
class DocumentElement(models.Model):
    """
    A top-level element in a rendered document.
    """
    parent   = models.ForeignKey(DocumentVersion)
    position = models.IntegerField(_("position in document"))
    text     = models.TextField(_("rendered text for this element"))
    
    class Meta:
        verbose_name = _("document element")
        verbose_name_plural = _("document elements")
        ordering = ('parent', 'position')
    
    def __unicode__(self):
        return self.text[:50]
        
        
class CommentStatus(models.Model):
    """
    A model to extend the attributes of contrib.comments.models.Comment.
    
    The link is created on comment creation by hooking on to the post_save
    signal.
    
    We did not simple extend the Comment class as doing so would require users
    to set their settings.COMMENT_APP to our app and effectively hijacking the
    whole contrib.comment apps. 
    
    We need to play nice as users may be using contrib.comments for other apps
    in their project.
    """
    STATE_NEW = 0
    STATE_ACKNOWLEDGED = 1
    
    comment_state_choices = (
        (STATE_NEW, _("New comment")),
        (STATE_ACKNOWLEDGED, _("Acknowledged by author")),
    )
    
    state = models.SmallIntegerField(_("state"), choices=comment_state_choices, default=STATE_NEW)
    comment = models.OneToOneField(Comment, related_name='doccomment_status')
    