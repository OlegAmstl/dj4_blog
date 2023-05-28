from django.urls import path

from .views import post_list, post_detail

app_name = 'blog_app'

urlpatterns = [
    path('', post_list, name='posts'),
    path('post/<int:id>/', post_detail, name='post_detail')
]
