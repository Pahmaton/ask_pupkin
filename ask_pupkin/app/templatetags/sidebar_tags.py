from django import template
from django.core.cache import cache

register = template.Library()

@register.inclusion_tag('sidebar.html')
def show_sidebar():
    return {
        'popular_tags': cache.get('popular_tags', []),
        'best_members': cache.get('best_members', []),
    }
