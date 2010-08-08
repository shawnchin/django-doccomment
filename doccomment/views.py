from django.shortcuts import render_to_response
from django.shortcuts import get_object_or_404
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.views.generic import list_detail
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseForbidden
from django.http import HttpResponseRedirect
from django.core.exceptions import SuspiciousOperation

from models import Document
from models import DocumentVersion
from models import DocumentElement
from forms import DocumentForm

# Get class to use for checking user permissions
from doccomment import get_permission_class
Permission = get_permission_class()
# Get class for parsing author input to HTML
from doccomment import get_parser_module
Parser = get_parser_module()

@user_passes_test(Permission.user_can_view_published)
def pub_list(request, template_name='doccomment/pub_list.html'):
    return render_to_response(template_name, {
        'doc_list' : Document.objects.published(),
    }, context_instance = RequestContext(request))

# shortcut to pub_view with latest version. permission check on pub_view
def pub_view_latest(request, id, slug):
    doc = get_object_or_404(Document.objects.published())
    return pub_view(request, id, slug, doc.latest_version)
    
@user_passes_test(Permission.user_can_view_published)
def pub_view(request, id, slug, ver, template_name='doccomment/pub_view.html'):
    # slug is ignored
    dv = get_object_or_404(DocumentVersion,
        document = id,
        version_string = ver,
    )
    return render_to_response(template_name, {
        'version' : dv,
    }, context_instance = RequestContext(request))
    
@user_passes_test(Permission.user_can_view_draft)
def draft_list(request, template_name='doccomment/draft_list.html'):
    return render_to_response(template_name, {
        'draft_list' : Document.objects.all(),
    }, context_instance = RequestContext(request))

@user_passes_test(Permission.user_can_view_draft)
def draft_preview(request, id, template_name='doccomment/draft_preview.html'):
    return render_to_response(template_name, {
        'draft' : get_object_or_404(Document, pk=id),
    }, context_instance = RequestContext(request))
    
@user_passes_test(Permission.user_is_author)
def draft_new(request, template_name='doccomment/doc_editor.html'):
    if request.method == 'POST':
        form = DocumentForm(request.POST)
        if form.is_valid():
            doc = form.save(commit=False)
            doc.author = request.user
            doc.save()
            if request.POST.get('save-and-continue', None):
                url = reverse('doccomment_draft_edit', kwargs={'id':doc.id})
            else:
                url = reverse('doccomment_draft_list')
            # TODO: use django-messages to display "saved" message
            return HttpResponseRedirect(url)
    else:
        form = DocumentForm()
    return render_to_response(template_name, {
        'form' : form,
    }, context_instance=RequestContext(request))
    
@user_passes_test(Permission.user_is_author)
def draft_edit(request, id, template_name='doccomment/doc_editor.html'):
    doc = get_object_or_404(Document, pk=id)
    if doc.author != request.user and not Permission.user_is_editor(request.user):
        return HttpResponseForbidden('You can only edit documents you created')
    if request.method == 'POST':
        form = DocumentForm(request.POST, instance=doc)
        if form.is_valid():
            doc = form.save(commit=False)
            doc.has_modification = True
            doc.save()
            if request.POST.get('save-and-continue', None):
                url = reverse('doccomment_draft_edit', kwargs={'id':doc.id})
            else:
                url = reverse('doccomment_draft_list')
            # TODO: use django-messages to display "saved" message
            return HttpResponseRedirect(url)
    else:
        form = DocumentForm(instance=doc)
    return render_to_response(template_name, {
        'form' : form,
        'document' : doc,
    }, context_instance=RequestContext(request))

@user_passes_test(Permission.user_is_author)
def draft_publish(request, id, ver):
    doc = get_object_or_404(Document, pk=id)
    if doc.author != request.user and not Permission.user_is_editor(request.user):
        return HttpResponseForbidden('You can only publish documents you created')
    if not ver in doc.next_version_choices:
        raise SuspiciousOperation
    pass
    
    # parse user input to HTML
    elements = Parser.parse_elements(doc.body)
    
    # create a snapshot of document as DocumentVersion
    dv = DocumentVersion(
        document = doc,
        title    = doc.title,
        body     = doc.body,
        author   = doc.author,
        rendered = "\n".join(elements),
        elem_count = len(elements),
        version_string = ver,
    )
    dv.save()
    
    # create records for each document elements
    for seq,txt in enumerate(elements):
        dv.documentelement_set.create(
            position = seq,
            text = txt,
        )
        
    # update version info in Document
    doc.published = True
    doc.date_published = dv.date_published
    doc.latest_version = dv.version_string
    doc.has_modification = False
    doc.save()
    
    # redirect to referring view, or fallback to preview page
    default_url = reverse('doccomment_draft_preview', kwargs={'id':doc.id})
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', default_url))