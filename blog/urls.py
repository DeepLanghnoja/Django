from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.home, name='blog-home'),
    path('category/<str:slug>', views.category, name='blog-category'),

    path('postComment', views.postComment, name="postComment"),
    path('<str:slug>', views.blogPost, name='blog-blogPost'),

]
