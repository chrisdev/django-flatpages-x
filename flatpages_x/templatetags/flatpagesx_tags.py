from django import template
from django.contrib.flatpages.models import FlatPage
from flatpages_x.models import FlatPageMeta,FlatPageImage

register = template.Library()

