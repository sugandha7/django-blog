from django.contrib.syndication.views import Feed
from blog.models import Post

class LatestPosts(Feed):
    title = "My Blog"
    link = "/blog/feed/"
    description = "Latest Posts"

    def items(self):
        return Post.objects.order_by('-created_on')[:5]

