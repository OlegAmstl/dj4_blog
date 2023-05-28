from django.shortcuts import render, get_object_or_404

from .models import Post


def post_list(request):
    """
    Отображение всех постов.
    :param request:
    :return:
    """
    template = "blog_app/post/list.html"
    posts = Post.published.all()
    context = {"posts": posts}
    return render(request, template, context=context)


def post_detail(request, id):
    """
    Отображение выбранного поста.
    :param request:
    :param id:
    :return:
    """
    template = "blog_app/post/detail.html"
    post = get_object_or_404(Post, id=id, status=Post.Status.PUBLISHED)
    context = {"post": post}
    return render(request, template, context=context)
