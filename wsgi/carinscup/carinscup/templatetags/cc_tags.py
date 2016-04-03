from django import template
from django.utils import timezone

from carinscup.models import Competitor

register = template.Library()


@register.assignment_tag
def get_members_with_results():
    members = Competitor.objects.filter(result__isnull=False).distinct()
    return members


@register.assignment_tag
def get_page_range(page_nr, nr_of_pages):
    tmp = range(1, nr_of_pages+1, 1)
    if nr_of_pages <= 5:
        return tmp
    if page_nr <= 3:
        return tmp[0:5]
    elif page_nr+2 >= nr_of_pages:
        return tmp[nr_of_pages-5:]
    else:
        return tmp[page_nr-3:page_nr+2]


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


@register.assignment_tag
def get_current_year():
    return timezone.now().year


@register.assignment_tag
def year_range():
    return range(2010, timezone.now().year+1, 1)
