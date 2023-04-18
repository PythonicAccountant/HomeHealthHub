from django.template import Library

register = Library()


@register.filter
def get_item(dictionary: dict, key: str):
    return dictionary.get(key)
