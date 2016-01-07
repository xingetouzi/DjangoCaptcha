#encoding:utf-8
from django.conf.urls import include, url, patterns

urlpatterns = patterns('main',
    ('^verify/','verify.views.display'),
)
