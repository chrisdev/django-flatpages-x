import re
import markdown
from markdown.inlinepatterns import IMAGE_REFERENCE_RE

from flatpages_x.models import FlatPageImage

img_ref_re = re.compile(IMAGE_REFERENCE_RE)


def parse(text):
    md = markdown.Markdown(['codehilite'])
    for iref in re.findall(img_ref_re, text):
        img_id = iref[7]
        try:
            image = FlatPageImage.objects.get(pk=int(img_id))
            md.references[img_id] = (image.image_path.url, '')
        except FlatPageImage.DoesNotExist:
            pass
    return md.convert(text)
