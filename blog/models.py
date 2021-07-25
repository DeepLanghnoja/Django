from django.db import models
from django.contrib.auth.models import User

from django.urls import reverse
from django.utils.timezone import now

from tinymce.models import HTMLField              

# Create your models here.

class Category(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    timeStamp = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def get_absolute_url(self):
        return reverse('blog:blog-category', args=[self.slug])

    def __str__(self):
        return self.title
    

class Post(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)
    content = HTMLField()
    timeStamp = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Posts'

    def get_absolute_url(self):
        return reverse('blog:blog-blogPost', args=[self.slug])

    def __str__(self):
        return self.title 


class BlogComment(models.Model):
    comment = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
    timeStamp = models.DateTimeField(default=now)

    class Meta:
        verbose_name_plural = 'Blog Comments'

    def __str__(self):
        return self.comment
    