from django.conf import settings
DEFAULT_TEMPLATE_CHOICES=[
       ('flatpages/default.html','Text Only',),
      ]
FPX_TEMPLATE_CHOICES=getattr(settings,'FLATPAGE_X_TEMPLATE_CHOICES',DEFAULT_TEMPLATE_CHOICES)


