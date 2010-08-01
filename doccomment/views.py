from django.shortcuts import render_to_response
from django.shortcuts import get_object_or_404
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.views.generic import list_detail
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseForbidden
from django.http import HttpResponseRedirect

from models import Document
from forms import DocumentForm

# Get class to use for checking user permissions
from doccomment import get_permission_class
Permission = get_permission_class()

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
    
@user_passes_test(Permission.user_can_create_draft)
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
    
@user_passes_test(Permission.user_can_create_draft)
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


