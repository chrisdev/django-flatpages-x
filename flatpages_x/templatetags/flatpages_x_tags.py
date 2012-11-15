from django import template

register = template.Library()


@register.inclusion_tag('flatpages_x/_metatag_snippet.html')
def show_meta(flatpage):
    ret = {
        "keywords": flatpage.metadata.keywords,
        "description": flatpage.metadata.description
    }
    return ret
