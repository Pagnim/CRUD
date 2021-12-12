from django.urls import path

from posts.views import PostView, ReadView, tests

urlpatterns = [
    path('/test', tests.as_view()),
    path('/post', PostView.as_view()),
    path('/read/<int:posts_id>', ReadView.as_view())
]