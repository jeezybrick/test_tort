__author__ = 'Jeezy'
from datetime import date, datetime
from django import template
from django.utils.timezone import is_aware, utc

register = template.Library()


@register.filter
def is_new_article(value):  # Only one argument.
    days_of_new_article = 3  # Дней при которых есть пометка new
    if not isinstance(value, date):  # datetime is a subclass of date
        return value

    now = datetime.now(utc if is_aware(value) else None)
    if value < now:
        delta = now - value
        if delta.days > days_of_new_article:
            return False
        else:
            return True
    else:
        return False