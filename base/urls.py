from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='base-home'),
    path('about/', views.about, name='base-about'),
    path('contact/', views.contact, name='base-contact'),
    path('search/', views.search, name='base-search'),

    path('author/<str:first_name>', views.handleAuthor, name='base-author'),

    path('signup', views.handleSignup, name='base-signup'),
    path('login', views.handleLogin, name='base-login'),
    path('logout/', views.handleLogout, name='base-logout'),
]
