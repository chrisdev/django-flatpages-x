from django import template
from django.contrib.flatpages.models import FlatPage
from flatpages_x.models import FlatPageMeta,FlatPageImage

register = template.Library()

@register.tag
def get_images(parser,token):
    """
    Gets all the images associated with the flatpage and stores them in a context variable
    The user may choose to exclude those images those as specified in the optional slug list.
    If the slug_list is not specified all the images will returned
    
    Usage:
    Retrieve all images associated with the flatpage
        {% get_images as context_var %}    
    Retrieve the images associated with the flatpage except those with slugs matching slug1,slug2.
        {% get_images exclude "xslug1,xslug2" as context_var %}   
    Retrieve the images associated with the flatpage only if they have slugs matching slug1,slug2.
        {% get_images include "xslug1,xslug2" as context_var %}       
    """
    bits = token.contents.split()
    slug_list=[]
    condition=None
    if len(bits) < 3:
        raise template.TemplateSyntaxError, "This tag requires at least 3 arguments"
    if len(bits) > 5:
        raise template.TemplateSyntaxError, "This tag requires no more than 4 arguments"    
    if bits[-2] != 'as':
        raise TemplateSyntaxError, "the second to last argument must be 'as'"
    if bits[1] != 'as':
        condition=bits[1]
        slug_list=bits[2].split(',')    
    return ImagesNode(condition,slug_list,bits[-1])

class ImagesNode(template.Node):
    def __init__(self,condition,slug_list,context_var):
        self.condition=condition
        self.slug_list=slug_list
        self.context_var=context_var
    def render(self,context):
        fp=context.get('flatpage')
        if self.condition is None:
            image_list=fp.objects.all()
        elif self.condition=='exclude':
            image_list=fp.images.all().exclude(slug__in=self.slug_list)
        else:
            image_list=fp.images.filter(slug__in=self.slug_list)
        
        context[self.context_var]=image_list
        return ''
