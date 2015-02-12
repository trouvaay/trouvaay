from django import template

register = template.Library()

@register.simple_tag
def url_replace(request, field, value):
    """Dynamic page generation for pagination
    """

    dict_ = request.GET.copy()

    dict_[field] = value

    return dict_.urlencode()