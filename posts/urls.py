from django.urls import path
from . import views

urlpatterns = [
    path('feed/', views.feed_view, name='feed'),
    path('posts/new/', views.create_post_view, name='create_post'),
    path('posts/<int:pk>/', views.post_detail_view, name='post_detail'),
    path('post/<int:post_id>/like/', views.toggle_like, name='toggle_like'),
]
