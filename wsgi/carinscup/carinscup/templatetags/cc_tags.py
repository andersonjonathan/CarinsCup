from django import template

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