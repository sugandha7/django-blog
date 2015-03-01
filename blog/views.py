from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect, render_to_response, get_object_or_404
from django.template import RequestContext
from django.views.generic.dates import MonthArchiveView
from django.views.generic.dates import WeekArchiveView
from django.views.generic.list import ListView
from django.core.paginator import Paginator, InvalidPage, EmptyPage
import time
from calendar import month_name
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from models import Post, Comment
from forms import PostForm, CommentForm
from config_vars import num_of_pages

def home(request):
    # Query the database for a list of ALL posts currently stored.
    # Order the posts by date in descending order.
    # Retrieve the top 5 only - or all if less than 5.
    # Place the list in our context_dict dictionary which will be passed to the template engine.
    post_list = Post.objects.order_by('-created_on')
    paginator = Paginator(post_list, num_of_pages)

    try: page = int(request.GET.get("page", '1'))
    except ValueError: page = 1

    try:
        posts = paginator.page(page)
    except (InvalidPage, EmptyPage):
        posts = paginator.page(paginator.num_pages)

    #context_dict = {'posts': posts, 'user': request.user}
    return render_to_response("blog/index.html", dict(posts=posts, user=request.user,
                                                post_list=posts.object_list, months=mkmonth_lst()))
    #return render_to_response('blog/index.html', context_dict, context_instance=RequestContext(request))

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
        return redirect(post)
    form.initial['name'] = request.session.get('name')
    form.initial['email'] = request.session.get('email')
    form.initial['website'] = request.session.get('website')
    return render_to_response('blog/blog_post.html',
                              {   'form': form, 
                                  'post': post,
                                  },
                              context_instance=RequestContext(request))

def delete_comment(request, slug, pk=None):
    """Delete comment(s) with primary key `pk` or with pks in POST."""
    if request.user.is_staff:
        if not pk: pklst = request.POST.getlist("delete")
        else: pklst = [pk]

        for pk in pklst:
            Comment.objects.get(pk=pk).delete()
        return HttpResponseRedirect(reverse("blog_post_detail", args=[slug]))

class PostWeekArchiveView(WeekArchiveView):
    queryset =Post.objects.all()
    date_field = "created_on"
    make_object_list = True
    week_format = "%W"
    allow_future = True
    template_name='blog/post_archive_week.html'

def mkmonth_lst():
    """Make a list of months to show archive links."""
    if not Post.objects.count(): return []

    # set up vars
    year, month = time.localtime()[:2]
    first = Post.objects.order_by("created_on")[0]
    fyear = first.created_on.year
    fmonth = first.created_on.month
    months = []

    # loop over years and months
    for y in range(year, fyear-1, -1):
        start, end = 12, 0
        if y == year: start = month
        if y == fyear: end = fmonth-1

        for m in range(start, end, -1):
            months.append((y, m, month_name[m]))
    return months

def month(request, year, month):
    """Monthly archive."""
    posts = Post.objects.filter(created_on__year=year, created_on__month=month)
    return render_to_response("blog/index.html", dict(post_list=posts, user=request.user,
                                                months=mkmonth_lst(), archive=True))
