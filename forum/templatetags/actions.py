from django.template.defaulttags import register


@register.simple_tag
def define(val=None):
    return val
