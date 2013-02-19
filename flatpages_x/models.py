from os.path import split
from datetime import datetime

from django.db import models
from django.contrib.flatpages.models import FlatPage
from django.utils.translation import ugettext_lazy as _
from filer.fields.image import FilerImageField
from filer.fields.file import FilerFileField
from django.utils.encoding import smart_unicode

# Create your models here.
class FlatPageMeta(models.Model):
    flatpage = models.OneToOneField(FlatPage, related_name="metadata")
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    keywords = models.CharField(blank=True, max_length=250,
                                help_text=_("Separate keywords by commas"))
    description = models.TextField(
        verbose_name=_('meta description'), blank=True)

    def __unicode__(self):
        return self.flatpage.title

    class  Meta:
        verbose_name = "Page MetaData"
        verbose_name_plural = "Page MetaData"


class FlatPageImage(models.Model):
    flatpage = models.ForeignKey(FlatPage, related_name='images')
    image = FilerImageField(null=True, blank=True)

    def __unicode__(self):

        return "![%s][%s]" % (self.image.label,
            self.image.pk
        )

    class Meta:
        verbose_name = "Image"
        verbose_name_plural = "Image"

class FlatPageAttachment(models.Model):

    flatpage = models.ForeignKey(FlatPage,
        related_name="attachments",
        blank=True, null=True
    )

    attachment = FilerFileField(null=True, blank=True)

    def __unicode__(self):

        return "[%s] [%s]" % (self.attachment.label,
            self.attachment.pk
        )

    class Meta:
        verbose_name = "Attachment"
        verbose_name_plural = "Attachments"



class Revision(models.Model):
    """
    Note the revision model stores the markdown while the
    flapage contents will store the redered html
    """
    flatpage = models.ForeignKey(FlatPage, related_name="revisions")
    title = models.CharField(max_length=90)
    content_source = models.TextField()

    updated = models.DateTimeField(default=datetime.now)

    view_count = models.IntegerField(default=0, editable=False)

    def __unicode__(self):
        return 'Revision %s for %s' % (self.updated.strftime('%Y%m%d-%H%M'), self.flatpage)

    def inc_views(self):
        self.view_count += 1
        self.save()
