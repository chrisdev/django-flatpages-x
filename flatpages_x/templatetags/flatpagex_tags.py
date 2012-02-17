from django import template
from django.contrib.flatpages.models import FlatPage
from flatpages_x.models import FlatPageMeta,FlatPageImage

register = template.Library()

@register.tag('meta_keywords')
def do_meta_keywords(parser, token):
    """
    Get the meta keywords associated with the flatpage and 
    stores them in a context_variable
    
    Usage:
    Get the keywords associated with the flat page
        {% meta_description as context_var  %}    
    """
    bits= token.split_contents()
    if len(bits) != 3:
        raise template.TemplateSyntaxError, "this tag takes 2 arguments" 
       
    return KeywordsNode(bits[-1])

class KeywordsNode(template.Node):
    def __init__(self, context_var):
        
        self.context_var=context_var
        
    def render(self, context):
        fp=context.get('flatpage')
        try:
            kw=FlatPageMeta.objects.filter(flatpage =fp)[0].keywords
        except IndexError:
            kw=''
        context[self.context_var]= kw
        return ''

@register.tag('meta_description')
def do_meta_description(parser, token):
    """
    Get the meta description tag associated with the flatpage a
    and stores it a context variable
    {% meta_description as [contex_var] %}
    """
    bits= token.split_contents()
    if len(bits) != 3:
        raise template.TemplateSyntaxError, "this tag takes 2 arguments"
    return MetaDescriptionNode(bits[-1])

class MetaDescriptionNode(template.Node):
    def __init__(self,var_name):
        self.var_name=var_name
    def render(self, context):
        fp=context.get('flatpage')
        try:
            des=FlatPageMeta.objects.filter(
                      flatpage = fp)[0].description
        except IndexError:
            des=''   
        context[self.var_name]= des
        return ' '

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
        print self.condition,self.slug_list,self.context_var
        fp=context.get('flatpage')
        if self.condition is None:
            print 'here'
            image_list=FlatPageImage.objects.filter(flatpage=fp)
        elif self.condition=='exclude':
            print 'there'
            image_list=FlatPageImage.objects.filter(flatpage=fp).exclude(slug__in=self.slug_list)
        else:
            print 'there'
            image_list=FlatPageImage.objects.filter(flatpage=fp,slug__in=self.slug_list)
            print image_list
        
        context[self.context_var]=image_list
        return ''
