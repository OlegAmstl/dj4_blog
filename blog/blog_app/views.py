from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView

from .models import Post


class PostList(ListView):
    queryset = Post.published.all()
    context_object_name = "posts"
    paginate_by = 3
    template_name = "blog_app/post/list.html"


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
    try:
        posts_list = paginator.page(page_number)
    except PageNotAnInteger:
        posts_list = paginator.page(1)
    except EmptyPage:
        posts_list = paginator.page(paginator.num_pages)
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
