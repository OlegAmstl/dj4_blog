from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator

from .models import Post


def post_list(request):
    """
    Отображение всех постов.
    :param request:
    :return:
    """
    template = "blog_app/post/list.html"
    posts = Post.published.all()
    paginator = Paginator(posts, 3)
    page_number = request.GET.get("page", 1)
    posts_list = paginator.page(page_number)
    context = {"posts": posts_list}
    return render(request, template, context=context)


def post_detail(request, year, month, day, post):
    """
    Отображение выбранного поста.
    :param request:
    :param id:
    :return:
    """
    template = "blog_app/post/detail.html"
    post = get_object_or_404(Post,
                             status=Post.Status.PUBLISHED,
                             slug=post,
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    context = {"post": post}
    return render(request, template, context=context)
