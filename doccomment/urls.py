from django.conf.urls.defaults import *

urlpatterns = patterns('doccomment.views',


    url(r'^$',
        view = 'pub_list',
        name = 'doccomment_pub_list',
    ),
    
    url(r'^(?P<id>\d+)/(?P<slug>[\w-]+)/$',
        view = 'pub_view_latest',
        name = 'doccumment_pub_view_latest',
    ),
    
    url(r'^(?P<id>\d+)/(?P<slug>[\w-]+)/(?P<ver>\d+\.\d+\.\d+)/$',
        view = 'pub_view',
        name = 'doccumment_pub_view',
    ),
    
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
    
    url(r'^draft/(?P<id>\d+)/publish/(?P<ver>\d+\.\d+\.\d+)/$',
        view = 'draft_publish',
        name = 'doccomment_draft_publish',
    ),
    
    url(r'^ajax/get-comment-count/(?P<v_id>\d+)/$',
        view = 'ajax_get_comment_count',
        name = 'doccomment_ajax_get_comment_count',
    ),
)