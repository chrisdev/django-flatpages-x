from os.path import split
from datetime import datetime

from django.db import models
from django.contrib.flatpages.models import FlatPage
from django.utils.translation import ugettext_lazy as _

# Thumbnailability
try:
    from sorl.thumbnail import ImageField
except ImportError:
    ImageField = models.ImageField


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
    image_path = ImageField(upload_to="flatpage/%Y/%m/%d")
    url = models.CharField(blank=True, max_length=150)

    def __unicode__(self):
        if self.pk is not None:
            img_file = split(self.image_path.url)[1]
            return "[%s] %s" % (self.pk, img_file)
        else:
            return "deleted image"


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
