from django import template
register = template.Library()

@register.filter
def index(indexable, i):
    return indexable[i]

@register.filter(name='range')
def filter_range(start, end):
    return range(start, end)