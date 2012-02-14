from setuptools import setup, find_packages

LONG_DESCRIPTION = """
===============================
Django Flatpage Extensions
===============================
Extensions to django.contrib.flatpages to allow for features such as meta tags and descriptions

Authors
--------

Quickstart
-----------


Forms
-----


 
Todo / Issues
--------------



"""
PACKAGE = "flatpages_x"
NAME = "django-flatpages-x"
DESCRIPTION = "Some Basic extensions for django-contrib-flatpages"
AUTHOR = "Chris Clarke"
AUTHOR_EMAIL = "cclarke@chrisdev.com"
URL = "http://github.com/chrisdev/django-flatpages-x"
VERSION = __import__(PACKAGE).__version__


setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    license="MIT",
    url=URL,
    packages=find_packages(exclude=["*.wpr","*.wpu"]),
    include_package_data=True,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Framework :: Django",
    ],
    zip_safe=False,
)
