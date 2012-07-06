===============================
Django Flatpage Extensions
===============================
An extension to django.contrib.flatpages to provide for 
 
- Support markdown and other similar markup formats. 
   You can also provide you own markup  format parser.
 
- Optional support for the excellent markTtUp jquery editor
   This requires the installation django-markitup.
   
- Easy inclusion of images in flatpages. Note Admin image thumbnails
   require the installation  of sorl thumbnails.
   
- The inclusion of metatag keywords and descriptions in flatpages.
 
- Some support for revisions.

Migrating you data to flapages_x should not be difficult since the
data which currently in the contrib.Flatpage model (content, titles) is not affected. 
Your templates will still utilize the  *{{flatpage.content}}* and *{{flatpage.body}}* 
context variables.
Once you installed flatpages_x the markdown formatted content
is actually be stored separately in a related Revisions model. 
On saving, this will be rendered to html via the configurable markdown and saved to
the Flatpage.content field
 
 
 
Contributors
-------------
* `Christopher Clarke <https://github.com/chrisdev>`_
* `Lendl Smith <https://github.com/ilendl2>`_



Quickstart
-----------
Create a virtual environment for your project and activate it::

    $ virtualenv mysite-env
    $ source mysite-env/bin/activate
    (mysite-env)$
    
Next install flatpages_x.::

    (mysite-env)$ pip install git+https://github.com/chrisdev/django-flatpages-x.git

Inside your project run::

    (mysite-env)$ python manage.py syncdb
    
**markItUp support**
   
If you want to use the excellent markItUp! editor widget. Install django-markitup
   
    (mysite-env)$ pip install django-markitup
    
You need a few configuration steps

1. Add 'markitup' to your INSTALLED_APPS setting.

2. Add the following to settings::

     MARKITUP_SET = 'markitup/sets/markdown'
     MARKITUP_SKIN = 'markitup/skins/markitup' 
     MARKITUP_FILTER = ('markdown.markdown', {'safe_mode': True})

3.You need to use the AJAX-based preview for the admin widget

     url(r'^markitup/', include('markitup.urls')) in your root URLconf.
     
**Admin thumbnails**    

If you want view admin image thumbnails install sorl thumbnails

    (mysite-env)$ pip install sorl-thumbnails
    
1. Add ``sorl.thumbnail`` to your ``settings.INSTALLED_APPS``.
2. Configure your ``settings``
3. If you are using the cached database key value store you need to sync the
   database::

    python manage.py syncdb






