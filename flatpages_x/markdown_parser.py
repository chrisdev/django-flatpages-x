import re
import markdown
from markdown.inlinepatterns import IMAGE_REFERENCE_RE, REFERENCE_RE
from .models import FlatPageImage, FlatPageAttachment
from filer.models import File
from django.core.exceptions import ObjectDoesNotExist
img_ref_re = re.compile(IMAGE_REFERENCE_RE)
reference_re = re.compile(REFERENCE_RE)

def parse(text):
    """
    This is a test of md references
    Ok now the ids
    ![Alt text 2][1]
    >>> parse('![Alt text 2][1]')
    u'<p><img alt="Alt text 2" src="/site_media/media/flatpage/2013/01/22/bottom-left2.gif" /></p>'

    parse('[an example] [1]')'

    """

    md = markdown.Markdown(['extra','codehilite'])

    for iref in re.findall(img_ref_re, text):
        img_id = iref[7]
        alt_txt = iref[0]
        try:
            fp_img= File.objects.get(pk=img_id)
            md.references[img_id] = (fp_img.url, alt_txt)
        except ObjectDoesNotExist:
           pass
   
    for lref in re.findall(reference_re, text):
        a_id = lref[7]
        alt_txt = lref[0]
        try:
            fa = File.objects.get(pk=a_id)
            md.references[a_id] = (fa.url, alt_txt)
        except ObjectDoesNotExist:
            pass


    return md.convert(text)

if __name__ == "__main__":
    #import doctest
    #doctest.testmod()
    #print parse('![Alt text 1][1]')
    print parse('[an example] [id] ')
