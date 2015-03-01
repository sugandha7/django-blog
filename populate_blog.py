import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'qblog.settings')

import django
django.setup()

from blog.models import Post
from django.contrib.auth.models import User
from content import blog_title, blog_content

def populate():
    user = User.objects.get(is_superuser=True)
    title = blog_title
    text = blog_content
    p = add_post(title, text, user)
    p.save()

def add_post(title, text, author):
    p = Post.objects.get_or_create(title=title, text=text, author= author)[0]
    return p


# Start execution here!
if __name__ == '__main__':
    print "Starting blog population script..."
    populate()
