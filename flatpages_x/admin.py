from datetime import datetime

from django import forms
from django.contrib import admin
from django.contrib.flatpages.admin import FlatPageAdmin as StockFlatPageAdmin, FlatpageForm
from django.contrib.flatpages.models import FlatPage
from django.utils.translation import ugettext_lazy as _
from django.utils.functional import curry

from flatpages_x.models import FlatPageImage, FlatPageMeta, Revision
from flatpages_x.settings import FPX_TEMPLATE_CHOICES
from flatpages_x.settings import PARSER
from flatpages_x.utils import load_path_attr

# Use markitup if available
try:
    from markitup.widgets import AdminMarkItUpWidget as content_widget
except ImportError:
    content_widget = forms.Textarea

# Thumbnails
try:
    from sorl.thumbnail import admin as thumbs
except ImportError:
    thumbs = None


class CustomFlatPageForm(FlatpageForm):
    template_name = forms.ChoiceField(
        choices=FPX_TEMPLATE_CHOICES, required=False,
        label='Template',
        help_text=_("Sepcify a template for displaying your content")
    )

    content_md = forms.CharField(label="Content", widget=content_widget())
    content = forms.CharField(widget=forms.Textarea(), required=False)

    def __init__(self, *args, **kwargs):
        super(CustomFlatPageForm, self).__init__(*args, **kwargs)
        fp = self.instance

        try:
            latest_revision = fp.revisions.order_by("-updated")[0]
        except IndexError:
            latest_revision = None

        if latest_revision:
            self.fields["content_md"].initial = latest_revision.content_source

    def save(self):
        fp = super(CustomFlatPageForm, self).save(commit=False)

        if PARSER:
            render_func = curry(load_path_attr(PARSER[0], **PARSER[1]))
            fp.content = render_func(self.cleaned_data["content_md"])
        else:
            fp.content = self.cleaned_data["content_md"]

        fp.save()

        r = Revision()
        r.flatpage = fp
        r.title = fp.title
        r.content_source = self.cleaned_data["content_md"]
        r.updated = datetime.now()
        r.save()

        return fp


class FlatPageMetaAdmin(admin.ModelAdmin):
    list_display = ('flatpage', 'created',)
    list_filter = ('flatpage',)
    ordering = ('flatpage',)
    search_fields = ('flatpage',)


admin.site.register(FlatPageMeta, FlatPageMetaAdmin)


class MetaInline(admin.StackedInline):
    model = FlatPageMeta


class ImageInline(admin.TabularInline):
    model = FlatPageImage

if thumbs is not None:
    # Add the mixin to the MRO
    class ImageInline(thumbs.AdminImageMixin, ImageInline):
        pass


class FlatPageAdmin(StockFlatPageAdmin):
    fieldsets = (
        (None, {'fields': ('url', 'title', 'content_md', 'template_name',)}),
        (_('Advanced options'), {'classes': ('collapse',),
                                 'fields': ('enable_comments', 'registration_required', 'sites')}),
    )
    form = CustomFlatPageForm
    inlines = [MetaInline,
               ImageInline,
               ]

    def save_form(self, request, form, change):
        # form.save doesn't take a commit kwarg
        return form.save()

admin.site.unregister(FlatPage)
admin.site.register(FlatPage, FlatPageAdmin)
admin.site.register(FlatPageImage)
admin.site.register(Revision)
