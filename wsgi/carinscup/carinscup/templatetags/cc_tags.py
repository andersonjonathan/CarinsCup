from django import template

from carinscup.models import Competitor

register = template.Library()


@register.assignment_tag
def get_members_with_results():
    members = Competitor.objects.filter(result__isnull=False).distinct()
    return members


@register.assignment_tag
def get_page_range(page_nr, nr_of_pages):
    if page_nr <= 3:
        return [1, 2, 3, 4, 5]
    elif page_nr+2 >= nr_of_pages:
        return [nr_of_pages-4, nr_of_pages-3, nr_of_pages-2, nr_of_pages-1, nr_of_pages]
    else:
        return [page_nr-2, page_nr-1, page_nr, page_nr+1, page_nr+2]