from django.conf.urls.defaults import *

urlpatterns = patterns('doccomment.views',

    url(r'^draft/list$',
        view = 'draft_list',
        name = 'doccomment_draft_list',
    ),
    
    url(r'^draft/new$',
        view = 'draft_new',
        name = 'doccomment_draft_new',
    ),
    
    url(r'^draft/(?P<id>\d+)/edit$',
        view = 'draft_edit',
        name = 'doccomment_draft_edit',
    ),
    
    url(r'^draft/(?P<id>\d+)/preview$',
        view = 'draft_preview',
        name = 'doccomment_draft_preview',
    ),
)