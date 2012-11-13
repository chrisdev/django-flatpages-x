from django.conf import settings

PARSER = getattr(settings, 'FLATPAGES_X_PARSER', None)
DEFAULT_TEMPLATE_CHOICES = [
    ('flatpages/default.html', 'Text Only', ),
]
FPX_TEMPLATE_CHOICES = getattr(
    settings, 'FLATPAGES_X_TEMPLATE_CHOICES', DEFAULT_TEMPLATE_CHOICES)
