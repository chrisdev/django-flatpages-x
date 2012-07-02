from django.conf import settings

PARSER = getattr(settings, "FLATPAGES_X_PARSER", ["flatpages_x.markdown_parser.parse", {}])
DEFAULT_TEMPLATE_CHOICES=[
       ('flatpages/default.html','Text Only',),
      ]
FPX_TEMPLATE_CHOICES=getattr(settings,'FLATPAGES_X_TEMPLATE_CHOICES',DEFAULT_TEMPLATE_CHOICES)


