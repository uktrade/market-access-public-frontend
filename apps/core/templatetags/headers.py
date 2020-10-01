from django import template

register = template.Library()


@register.inclusion_tag("partials/content_header.html")
def content_header(title, caption=None, size="xl"):
    return {
        "caption": caption,
        "title": title,
        "size": size
    }
