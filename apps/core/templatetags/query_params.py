from urllib.parse import parse_qs, urlencode

from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def location_filter(context, location):
    query_string = context.get("query_string")
    if query_string:
        query_string = f'?{query_string}&location={location}'
    else:
        query_string = f'?location={location}'

    return query_string


@register.simple_tag(takes_context=True)
def sector_filter(context, sector):
    query_string = context.get("query_string")
    if query_string:
        query_string = f'?{query_string}&sector={sector}'
    else:
        query_string = f'?sector={sector}'

    return query_string


@register.simple_tag(takes_context=True)
def remove_filter(context, filter_name):
    params = parse_qs(context.get("query_string"))
    params.pop(filter_name, None)
    query_string = f"?{urlencode(params, doseq=True)}"
    return query_string
