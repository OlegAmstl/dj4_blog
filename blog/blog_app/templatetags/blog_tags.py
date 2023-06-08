from django import template
from django.db.models import Count
from django.utils.safestring import mark_safe
import markdown
from ..models import Post

register = template.Library()


@register.simple_tag
def total_posts():
    """
    Показывает общее количество постов.
    """
    return Post.published.count()


@register.inclusion_tag('blog_app/post/latest_posts.html')
def show_latest_posts(count=5):
    """
    Показывает последние 5 постов.
    """
    latest_posts = Post.published.order_by('-publish')[:count]
    return {'latest_posts': latest_posts}


@register.simple_tag
def get_most_commented_posts(count=5):
    """
    Отображает 5 постов у которых больше всего комментариев.
    """
    return Post.published.annotate(
        total_comments=Count('comments')).order_by('-total_comments')[:count]


@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(text))
