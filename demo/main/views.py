#encoding:utf-8
from django.http import HttpResponse
import Image,ImageDraw,ImageFont,random,StringIO
import os
from django.shortcuts import render_to_response as render
from DjangoCaptcha import Captcha

def code(request):
    ca =  Captcha(request)
    ca.worlds = ['hello','world','helloworld']
    ca.type = 'number'
    ca.type = 'word'
    return ca.display()

def index(request):
    _code = request.GET.get('code') or ''
    if not _code:
        return render('index.html',locals())

    ca = Captcha(request)
    if ca.check(_code):
        return HttpResponse("""<h1>^_^</h1>""")
    return HttpResponse("""<h1>:-(</h1>""")

