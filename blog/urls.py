from django.conf.urls import patterns, url, include
from models import Post
from blog.views import  PostWeekArchiveView
from blog import  feed


urlpatterns = patterns('',
    url(r'^post/(?P<slug>[-\w]+)$', 
        'blog.views.view_post',
        name='blog_post_detail'),
    url(r'^add/post$', 
        'blog.views.add_post', 
        name='blog_add_post'),
    url(r'^archive/week/(?P<year>\d+)/(?P<week>\d+)$',
        PostWeekArchiveView.as_view(),
        name='blog_archive_week',
       ),
    url(r'^$', 'blog.views.home', name='blog'),
    url(r'^month/(?P<year>\d+)/(?P<month>\w+)$',
        'blog.views.month',
        name='blog_month',
       ),
    url(r'^delete_comment/(?P<slug>[-\w]+)/(\d+)$', 
        'blog.views.delete_comment',
        name='blog_delete_comment'),
    url(r'^delete_comment/(?P<slug>[-\w]+)$', 
        'blog.views.delete_comment',
        name='blog_delete_all_comments'),
    url(r'^feed/$', feed.LatestPosts(), name="feed"),
)
