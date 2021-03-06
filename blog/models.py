from django.db import models
from django.template.defaultfilters import slugify
from django.core.urlresolvers import reverse

from django.contrib.auth.models import User

# Create your models here.
class Tag(models.Model):
    slug = models.SlugField(max_length=200, unique=True)

    def __str__(self):
        return self.slug
        
class Post(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    text = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User)
    tags = models.ManyToManyField(Tag)

    def __unicode__(self):
        return self.title

   #@models.permalink
    def get_absolute_url(self):
    	return reverse("blog_post_detail", kwargs={"slug": self.slug})
        #return ('blog_post_detail', (), 
         #       {
          #          'slug' :self.slug,
           #     })

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)

class Comment(models.Model):
    name = models.CharField(max_length=42)
    email = models.EmailField(max_length=75)
    website = models.URLField(max_length=200, null=True, blank=True)
    text = models.TextField()
    post = models.ForeignKey(Post)
    created_on = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.text

