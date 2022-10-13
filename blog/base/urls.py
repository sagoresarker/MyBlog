from . import views
from django.urls import path, include
from .feeds import LatestPostsFeed


urlpatterns = [
    path('', views.home, name='home'),
    path('posts/', views.PostList, name='allpost'),
    path('<slug:slug>/', views.post_detail, name='post_detail'),
    path("feed/rss", LatestPostsFeed(), name="post_feed"),

]

