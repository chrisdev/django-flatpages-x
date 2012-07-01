from django.contrib import admin
from django.contrib.flatpages.admin import FlatPageAdmin as StockFlatPageAdmin,FlatpageForm
from django.contrib.flatpages.models import FlatPage
from django import forms
from django.utils.translation import ugettext_lazy as _
from flatpages_x.models import FlatPageImage,FlatPageMeta
from flatpages_x.settings import FPX_TEMPLATE_CHOICES
from django.utils.functional import curry
from flatpages_x.settings import PARSER
from flatpages_x.utils import load_path_attr



class CustomFlatPageForm(FlatpageForm):
    template_name=forms.ChoiceField(choices=FPX_TEMPLATE_CHOICES, required=False,
                                    label='Template',
                                    help_text=_("Sepcify a template for displaying your content")
                                )
    
    def save(self):
        fp= super(CustomFlatPageForm, self).save(commit=False)
        render_func = curry(load_path_attr(PARSER[0],**PARSER[1]))
        fp.content= render_func(self.cleaned_data["content"])
        fp.save()
        return fp 
      
      
class FlatPageMetaAdmin(admin.ModelAdmin):
    list_display = ('flatpage','created',)
    list_filter = ('flatpage',)
    ordering = ('flatpage',)
    search_fields = ('flatpage',)
         

admin.site.register(FlatPageMeta, FlatPageMetaAdmin)

class MetaInline(admin.StackedInline):
    model = FlatPageMeta
class ImageInline(admin.TabularInline):
    model=FlatPageImage  
    
    
    
class FlatPageAdmin(StockFlatPageAdmin):
    fieldsets= (
        (None, {'fields': ('url', 'title', 'content', 'template_name',)}),
        (_('Advanced options'), {'classes': ('collapse',), 
        'fields': ('enable_comments', 'registration_required','sites' )}),
    )
    form=CustomFlatPageForm
    inlines = [MetaInline,
               ImageInline,
               ]
    
    def save_form(self, request, form, change):
        # form.save doesn't take a commit kwarg
        return form.save() 
    
admin.site.unregister(FlatPage)
admin.site.register(FlatPage, FlatPageAdmin)
admin.site.register(FlatPageImage)