#!/bin/bash
if [ ! -n "$1" ]; then
    ENV="dev" 
else
    ENV=$1
fi

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
export PYTHONPATH=$DIR:$PYTHONPATH
export DJANGO_SETTINGS_MODULE="settings"
source `which virtualenvwrapper.sh`
workon django-captcha
export ENV=${ENV}
