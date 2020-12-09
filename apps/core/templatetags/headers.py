from django import template

register = template.Library()


@register.inclusion_tag("partials/content_header.html")
def content_header(title, caption=None, size="xl", below=False):
    if not caption:
        below = False
    above = not below
    return {
        "caption": caption,
        "above": above,
        "below": below,
        "title": title,
        "size": size,
    }
