from django.template import Library
from django.db.models import Sum

register = Library()

@register.filter
def get_item(dictionary: dict, key: str):
    return dictionary.get(key)
