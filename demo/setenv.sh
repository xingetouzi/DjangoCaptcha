#!/bin/bash
apt-get install -y libjpeg-dev  libpng12-dev git-core git redis-server python-setuptools python-dev 
easy_install pip
pip install virtualenvwrapper
source `which virtualenvwrapper.sh`

mkvirtualenv django-captcha
workon django-captcha
pip install -r requirements.txt
