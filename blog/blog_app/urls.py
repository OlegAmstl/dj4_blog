from django.urls import path

from .views import post_detail, PostList, post_comment

app_name = 'blog_app'

urlpatterns = [
    path('', PostList.as_view(), name='posts'),
    path('post/<int:year>/<int:month>/<int:day>/<slug:post>/',
         post_detail, name='post_detail'),
    path('post/<int:post_id>/comment/', post_comment, name='post_comment')
]
