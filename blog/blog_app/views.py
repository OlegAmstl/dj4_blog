from django.core.paginator import PageNotAnInteger, EmptyPage, Paginator
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_POST
from django.db.models import Count
from taggit.models import Tag

from .models import Post
from .forms import EmailPostForm, CommentForm


# class PostList(ListView):
#     """
#     Отображение всех постов
#     """
#     queryset = Post.published.all()
#     context_object_name = "posts"
#     paginate_by = 3
#     template_name = "blog_app/post/list.html"


def post_list(request, tag_slug=None):
    """
    Отображение всех постов.
    :param request:
    :return:
    """
    template = "blog_app/post/list.html"
    posts = Post.published.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        posts = posts.filter(tags__in=[tag])
    paginator = Paginator(posts, 3)
    page_number = request.GET.get("page", 1)
    try:
        posts_list = paginator.page(page_number)
    except PageNotAnInteger:
        posts_list = paginator.page(1)
    except EmptyPage:
        posts_list = paginator.page(paginator.num_pages)
    context = {"posts": posts_list,
               "tag": tag}
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
    comments = post.comments.filter(active=True)

    # Формв комментариев
    form = CommentForm()

    # Список схожих постов
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(
        tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(
        same_tags=Count('tags')).order_by('-same_tags', '-publish')[:4]
    context = {"post": post,
               "comments": comments,
               "form": form,
               "similar_posts": similar_posts}
    return render(request, template, context=context)


def post_share(request, post_id):
    """
    Представление отправки поста по email.
    :param request:
    :param post_id:
    :return:
    """
    template = "blog_app/post/share.html"
    post = get_object_or_404(Post,
                             id=post_id,
                             status=Post.Status.PUBLISHED)
    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
    else:
        form = EmailPostForm()
    context = {
        "post": post,
        "form": form
    }
    return render(request, template, context=context)


@require_POST
def post_comment(request, post_id):
    """
    Представление коментария в посте.
    :param request:
    :param post_id:
    :return:
    """
    template = "blog_app/post/comment.html"
    post = get_object_or_404(Post,
                             id=post_id,
                             status=Post.Status.PUBLISHED)
    comment = None
    form = CommentForm(data=request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()
    context = {
        "post": post,
        "form": form,
        "comment": comment
    }
    return render(request, template, context=context)
