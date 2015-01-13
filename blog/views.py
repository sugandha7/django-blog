from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect, render_to_response, get_object_or_404
from django.template import RequestContext
from django.views.generic.dates import MonthArchiveView
from django.views.generic.dates import WeekArchiveView


from models import Post
from forms import PostForm, CommentForm

@user_passes_test(lambda u: u.is_superuser)
def add_post(request):
    form = PostForm(request.POST or None)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect(post)
    return render_to_response('blog/add_post.html', 
                              { 'form': form },
                              context_instance=RequestContext(request))

def view_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()
        request.session["name"] = comment.name
        request.session["email"] = comment.email
        request.session["website"] = comment.website
        return redirect(request.path)
    form.initial['name'] = request.session.get('name')
    form.initial['email'] = request.session.get('email')
    form.initial['website'] = request.session.get('website')
    return render_to_response('blog/blog_post.html',
                              {
                                  'post': post,
                                  'form': form,
                              },
                              context_instance=RequestContext(request))

class PostMonthArchiveView(MonthArchiveView):
    queryset = Post.objects.all()
    date_field = "created_on"
    make_object_list = True
    allow_future = True
    month_format='%m'
    template_name='blog/post_archive_month.html'

class PostWeekArchiveView(WeekArchiveView):
    queryset =Post.objects.all()
    date_field = "created_on"
    make_object_list = True
    week_format = "%W"
    allow_future = True
    template_name='blog/post_archive_week.html'
