#encoding:utf-8
from django.http import HttpResponse
from django.shortcuts import render_to_response as render
from DjangoCaptcha import Captcha

def code(request):
    ca =  Captcha(request)
    #ca.words = ['hello','world','helloworld']
    ca_type = request.GET.get('type', 'word').lower()
    assert ca_type in ['number', 'word']

    ca.type = ca_type
    ca.img_width = 250
    ca.img_height = 40
    return ca.display()

def index(request):
    ca_type = request.GET.get('type', 'word').lower()
    assert ca_type in ['number', 'word']

    _code = request.GET.get('code') or ''
    if not _code:
        return render('index.html',locals())

    ca = Captcha(request)
    if ca.validate(_code):
        return HttpResponse("""<h1>^_^</h1><a href="/">back</a>""")
    return HttpResponse("""<h1>:-(</h1><a href="/">back</a>""")

