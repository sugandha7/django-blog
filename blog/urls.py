from django.conf.urls import patterns, url, include
from models import Post
from blog.views import PostMonthArchiveView, PostWeekArchiveView

urlpatterns = patterns('',
    url(r'^post/(?P<slug>[-\w]+)$', 
        'blog.views.view_post',
        name='blog_post_detail'),
    url(r'^add/post$', 
        'blog.views.add_post', 
        name='blog_add_post'),
    url(r'^archive/month/(?P<year>\d+)/(?P<month>\w+)$',
        PostMonthArchiveView.as_view(),
        name='blog_archive_month',
       ),
    url(r'^archive/week/(?P<year>\d+)/(?P<week>\d+)$',
        PostWeekArchiveView.as_view(),
        name='blog_archive_week',
       ),
)
