from django import template
from ..models import Post


register = template.Library()

@register.simple_tag
def total_posts():
    """
    Показывает общее количество постов.
    """
    return Post.published.count()