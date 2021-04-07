from django import template
import random

register = template.Library()

@register.filter
def shuffle_list(value):
    content = list(value)

    return random.sample(content, 3)