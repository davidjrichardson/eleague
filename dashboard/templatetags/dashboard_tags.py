from math import floor

from django import template
from django.core.paginator import Page

register = template.Library()


@register.filter
def paginator_range(page: Page, length: int = 5):
    source_paginator = page.paginator

    if source_paginator.num_pages <= length:
        return page.paginator.page_range
    else:
        lower_bound = page.number - floor(length / 2)
        upper_bound = page.number + floor(length / 2)

        if lower_bound < 1:
            upper_bound = upper_bound + (1 - lower_bound)
            lower_bound = 1

        if upper_bound > source_paginator.num_pages:
            lower_bound = lower_bound - (upper_bound - source_paginator.num_pages)
            upper_bound = source_paginator.num_pages

        return range(lower_bound, upper_bound + 1)
