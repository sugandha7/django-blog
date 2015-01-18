from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect, render_to_response, get_object_or_404
from django.template import RequestContext
from django.views.generic.dates import MonthArchiveView
from django.views.generic.dates import WeekArchiveView
from django.views.generic.list import ListView
from django.core.paginator import Paginator, InvalidPage, EmptyPage


from models import Post
from forms import PostForm, CommentForm

def home(request):
    # Query the database for a list of ALL posts currently stored.
    # Order the posts by date in descending order.
    # Retrieve the top 5 only - or all if less than 5.
    # Place the list in our context_dict dictionary which will be passed to the template engine.
    post_list = Post.objects.order_by('-created_on')
    paginator = Paginator(post_list, 2)

    try: page = int(request.GET.get("page", '1'))
    except ValueError: page = 1

    try:
        posts = paginator.page(page)
    except (InvalidPage, EmptyPage):
        posts = paginator.page(paginator.num_pages)

    context_dict = {'posts': posts, 'user': request.user}
    return render_to_response('blog/index.html', context_dict, context_instance=RequestContext(request))

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

    return render_to_response('blog/blog_post.html',
                              {
                                  'post': post,
                                  },
                              context_instance=RequestContext(request))

def add_comment(request, slug):
    post = get_object_or_404(Post, slug=slug)
    form = CommentForm(request.POST or None)
    
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()
        request.session["name"] = comment.name
        request.session["email"] = comment.email
        request.session["website"] = comment.website
        return redirect(post)
    form.initial['name'] = request.session.get('name')
    form.initial['email'] = request.session.get('email')
    form.initial['website'] = request.session.get('website')
    return render_to_response('blog/add_comment.html',
                              {
                                  'form': form,
                                  },
                              context_instance=RequestContext(request))
def post_list(request, page=0, paginate_by=3):

    return ListView.as_view(
        request,
        queryset=Post.objects.all(),
        paginate_by=paginate_by,
        page=page
    )

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
