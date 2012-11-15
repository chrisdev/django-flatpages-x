#!/bin/sh
# django-flatpages-x shell script to upload to pypi.

WORKDIR=/tmp/django-flatpages-x-build.$$
mkdir $WORKDIR
pushd $WORKDIR

git clone git://github.com/chrisdev/django-flatpages-x.git
cd django-flatpages-x

/usr/bin/python setup.py sdist upload

popd
rm -rf $WORKDIR