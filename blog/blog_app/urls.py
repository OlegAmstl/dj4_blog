from django.urls import path

from .views import post_detail, post_list, post_comment
from .feeds import LatestPostsFeed

app_name = 'blog_app'

urlpatterns = [
    path('', post_list, name='posts'),
    path('post/<int:year>/<int:month>/<int:day>/<slug:post>/',
         post_detail, name='post_detail'),
    path('post/<int:post_id>/comment/', post_comment, name='post_comment'),
    path('tag/<slug:tag_slug>/', post_list, name='post_list_by_tag'),
    path('feed/', LatestPostsFeed(), name='post_feed')
]
