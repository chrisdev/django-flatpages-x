from django.db import models
from django.conf import settings
from django.contrib.flatpages.models import FlatPage
from datetime import datetime
from django.utils.translation import ugettext_lazy as _


# Create your models here.
class FlatPageMeta(models.Model):
    flatpage=models.OneToOneField(FlatPage)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    keywords=models.CharField(blank=True,max_length=250,
                              help_text= _("Seperate keywords by commas") )
    description=models.TextField(verbose_name=_('meta description'),blank=True)
    
    
    def __unicode__(self):
        return self.flatpage.title
    
    class  Meta:
        verbose_name="Page MetaData"
        verbose_name_plural="Page MetaData"
        
    
    
    
class FlatPageImage(models.Model):
    flatpage=models.ForeignKey(FlatPage, related_name='images')
    image_path = models.ImageField(upload_to="flatpage/%Y/%m/%d")
    slug=models.SlugField(max_length=100)
    caption=models.CharField(max_length=120,blank=True)
    timestamp = models.DateTimeField(default=datetime.now, editable=False)
    
    url = models.CharField(blank=True,max_length=150)
    
    def __unicode__(self):
            if self.pk is not None:
                return "%s" % self.image_path
            else:
                return "deleted image"    
    
    class Meta:
        unique_together=('flatpage','slug')
    
    
