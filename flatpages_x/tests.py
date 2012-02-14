from django.template import Template, Context, TemplateSyntaxError
from django.test import TestCase
from django.contrib.flatpages.models import FlatPage
from flatpage_x.models import FlatPageImage,FlatPageMeta

class FpxTestCase(TestCase):
    fixtures = ['test_data']
    def setUp():
        self.fp=FlatPage.objects.all()[0]
    
    def test_flapage_objects(self):
        fp.images.all()
