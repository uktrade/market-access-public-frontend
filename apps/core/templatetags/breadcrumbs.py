from django import template
from django.urls import reverse

register = template.Library()


DEFAULT_BREADCRUMBS = (
    ("Home", "https://www.gov.uk/"),
    ("Find barriers", reverse("barriers:find-barriers-splash"))
)
ACTIVE_BREADCRUMB_CSS_CLASS = " govuk-breadcrumbs__list-item--active"


@register.inclusion_tag("partials/breadcrumbs.html", takes_context=True)
def show_breadcrumbs(context, items=()):
    """
    Accepts a list of tuples to build breadcrumbs.
    :param context: django context
    :param items: LIST of TUPLES (text, href)
    :return: DICT for the template
    """
    breadcrumbs = []
    current_path = context["request"].path
    for i in (*DEFAULT_BREADCRUMBS, *items):
        text, href = i
        d = {
            "text": text,
            "href": href
        }
        if current_path == href:
            d["css_classes"] = ACTIVE_BREADCRUMB_CSS_CLASS
        breadcrumbs.append(d)

    return {
        "breadcrumbs": breadcrumbs
    }
