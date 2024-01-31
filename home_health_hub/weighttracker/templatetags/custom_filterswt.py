import calendar

from django.template import Library

register = Library()


@register.filter
def month_name(month_number):
    return calendar.month_name[month_number]
