from django.urls import path

from posts.views import PostView, ReadView

urlpatterns = [
    path('/post', PostView.as_view()),
    path('/read/<int:posts_id>', ReadView.as_view())
]