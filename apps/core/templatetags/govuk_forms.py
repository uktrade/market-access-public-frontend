from django import template

FORM_GROUP_CLASSES = "govuk-form-group"
FORM_GROUP_ERROR_CLASSES = "govuk-form-group--error"

register = template.Library()


@register.simple_tag()
def form_group_classes(*args):
    """Used to set CSS classes for a form group"""
    classes = [FORM_GROUP_CLASSES]
    for arg in args:
        if arg:
            classes.append(FORM_GROUP_ERROR_CLASSES)
    return " ".join(set(classes))


@register.inclusion_tag("partials/forms/field_error.html")
def form_field_error(arg1, arg2=None):
    if arg2 is None:
        field = arg1
        return {"errors": field.errors}

    form = arg1
    field_name = arg2
    return {"errors": form.errors.get(field_name)}


@register.inclusion_tag("partials/forms/radio_input.html")
def radio_input(field, classes=None, legend_classes=None, radio_classes=None):
    return {
        "field": field,
        "classes": classes,
        "legend_classes": legend_classes or "govuk-fieldset__legend--m",
        "radio_classes": radio_classes
    }


@register.inclusion_tag("partials/forms/textarea.html")
def textarea(field, character_count=False, classes=None, label_classes=None):
    return {
        "field": field,
        "character_count": character_count,
        "classes": classes,
        "label_classes": label_classes
    }
