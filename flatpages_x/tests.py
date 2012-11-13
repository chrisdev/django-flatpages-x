from django.test import TestCase
from django.contrib.flatpages.models import FlatPage


class FpxTestCase(TestCase):
    fixtures = ['test_data', ]

    def setUp(self):
        self.fp = FlatPage.objects.all()[0]

    def test_flapage_objects(self):
        self.fp.images.all()
