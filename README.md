DjangoCaptcha 
=======================
介绍
----
在django中生成英文单词验证码,提供验证码图片生成,检查验证码等功能
原用于[pythoner.net](http://pythoner.net)的验证码,现整理出来打包发布到pypi.

#### 新特性
+ 新增数字验证码模式
+ 字体尺寸根据图片长宽自适应


Usage
---
####Install####
```
pip install DjangoCaptcha
or
easy_install DjangoCaptcha
```
####Display(views.py)####
```
from DjangoCaptcha import Code
def code(request):
    code =  Code(request)
    code.words = ['hello','world','helloworld']
    code.type = 'number'
    return code.display()
```

####Check user input(views.py)####
```
from DjangoCaptcha import Code
def index(request):
    _code = request.GET.get('code') or ''
    if not _code:
        return render('index.html',locals())

    code = Code(request)
    if code.check(_code):
        return HttpResponse('验证成功')
    else:
        return HttpResponse('验证失败')
```

Custom
-----
##### width of image
`code.img_width` = 150
##### height of image 
`code.img_height` = 30
##### type fo code ('number'/'word')
`code.type = 'number'`

Rely on
----
+ PIL

More
----
+ <http://pythoner.net>
