from . import views
from django.urls import path, include


urlpatterns = [
    path('', views.PostList, name='home'),
    path('<slug:slug>/', views.post_detail, name='post_detail'),

]

