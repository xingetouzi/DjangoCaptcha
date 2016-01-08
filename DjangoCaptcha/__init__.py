#encoding:utf-8

"""
Copyright 2013 TY<tianyu0915@gmail.com>

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

"""

from django.http import HttpResponse
from PIL import Image,ImageDraw,ImageFont
import random,StringIO
import os
import math

__version__ = '0.3.1',  

current_path = os.path.normpath(os.path.dirname(__file__))

class Captcha(object):

    def __init__(self,request):
        """ something init
        """

        self.django_request = request
        self.session_key = '_django_captcha_key'
        self.words = []

        # image size (pix)
        self.img_width = 150
        self.img_height = 30

        # default type
        self.type = 'number' 

        self._sin_y_dict = {}


    @property
    def font_size(self):
        """  将图片高度的80%作为字体大小
        """
        return int(math.ceil(self.img_height * 0.6))
    
    def _get_roate_value(self, letter):
        """ 获取字符的旋转角度
        """
        letter = str(letter)

        # 某些字符不需要旋转
        not_roate = ['q', 'g', 'p', 'b', 'd', 'y']
        if letter in not_roate:
            return 0

        # 有1/2的几率需要旋转
        if random.randint(0, 1) == 1:
            return random.randint(-15, 15)
        return 0

    def _get_words(self):
        """ The words list
        """

        # TODO  扩充单词表

        if self.words:
            return set(self.words)

        file_path = os.path.join(current_path,'words.list')
        f = open(file_path,'r')
        return set([line.replace('\n','') for line in f.readlines()])

    def _set_answer(self,answer):
        """  设置答案
        
        """
        self.django_request.session[self.session_key] = str(answer)

    def _yield_code(self):
        """  生成验证码文字,以及答案
        
        """

        # 英文单词验证码
        def word():
            code = random.sample(self._get_words(), 1)[0]
            self._set_answer(code)
            return code


        # 数字公式验证码
        def number():
            m,n = 1,50
            x = random.randrange(m,n)
            y = random.randrange(m,n)

            r = random.randrange(0,2)
            if r == 0:
                code = "%s - %s = ?" %(x,y)
                z = x - y
            else:
                code = "%s + %s = ?" %(x,y)
                z = x + y
            self._set_answer(z)
            return code

        fun = eval(self.type.lower())
        return fun()

    def _rotate(self, img, n):
        """ 旋转图像
        """

        im2 = img.convert('RGBA')
        # rotated image
        rot = im2.rotate(n, expand=1)
        # a white image same size as rotated image
        fff = Image.new('RGBA', rot.size, (255,)*4)
        # create a composite image using the alpha layer of rot as a mask
        out = Image.composite(rot, fff, rot)
        # save your work (converting back to mode='1' or whatever..)
        return out.convert(img.mode)

    def _draw_text(self, draw, position, text, font, fill, padding=1, outline='white'):
        """ 画描边字体
        """
        x, y = position
        
        # 画描边
        draw.text((x, y+1), text, font=font, fill=outline)
        draw.text((x, y-1), text, font=font, fill=outline)
        draw.text((x+1, y), text, font=font, fill=outline)
        draw.text((x+1, y+1), text, font=font, fill=outline)
        draw.text((x+1, y-1), text, font=font, fill=outline)
        draw.text((x-1, y), text, font=font, fill=outline)
        draw.text((x-1, y+1), text, font=font, fill=outline)
        draw.text((x-1, y-1), text, font=font, fill=outline)

        draw.text((x, y), text, font=font, fill=fill)

    def _gen_sin_y_dict(self):
        if self._sin_y_dict:
            return self._sin_y_dict

        delta = random.randrange(0, 100)
        for x in range(self.img_width):
            y = (math.sin(0.04*x + delta) + 1) * self.img_height
            y = y/5.0 + 10
            self._sin_y_dict[x] = y
        return self._sin_y_dict


    def display(self):
        """  The captch image output using Django response object
        """

        # font color
        self.font_color = ['black','darkblue','darkred']

        # background color
        #self.background = (random.randrange(230,255),random.randrange(230,255),random.randrange(230,255))
        self.background = (random.randrange(0,50),random.randrange(0,50),random.randrange(0, 50))

        # font path
        #self.font_path = os.path.join(current_path,'timesbi.ttf')
        self.font_path = os.path.join(current_path,'Menlo.ttc')

        # clean sesson
        self.django_request.session[self.session_key] = '' 

        # creat a image picture
        im = Image.new('RGB',(self.img_width,self.img_height),self.background)
        self.code = self._yield_code()
        draw = ImageDraw.Draw(im)

        # noise
        sin_y_dict = self._gen_sin_y_dict()
        for x in range(self.img_width):
            # 按照函数图像走势画干扰点
            if random.randint(1, 2) == 1:
                py = random.randrange(int(0.2*self.img_height), int(0.8*self.img_height))
                py = sin_y_dict[x] + random.randint(-int(0.4*self.img_height), int(0.4*self.img_height))

                fill = random.choice(['white', 'black'])
                box = random.choice([(x,py,x+2,py+2), (x,py,x+1,py+2), (x,py,x+2,py+1)])
                draw.rectangle(box, fill=fill)

            # 画辅助线
            #draw.point((x,y), fill=fill)


        # code part
        j = int(self.font_size*0.3)
        k = self.img_width - self.font_size * len(self.code) * 0.5
        k = int(k)
        delta_x = random.randrange(j, k) #starts point
        for i in self.code:
            # 有一半的几率旋转字符
            rotate_value = self._get_roate_value(i)

            i_im = Image.new('RGBA',(self.font_size, self.font_size), (0,0,0,0))
            i_draw = ImageDraw.Draw(i_im)
            
            font = ImageFont.truetype(self.font_path.replace('\\','/'), self.font_size)
            fill=random.choice(self.font_color)
            # 画描边字体
            self._draw_text(i_draw, (0, 0), i, font, fill)
            
            # 旋转字符
            i_im = i_im.rotate(rotate_value, expand=1).resize(i_im.size) if rotate_value > 0 else i_im

            # 跟随函数曲线上下抖动
            delta_y = int(math.ceil(sin_y_dict[int(delta_x)] * 0.5) - i_im.height/2.0)
            
            box = (delta_x, delta_y, delta_x+i_im.width, delta_y+i_im.height)
            im.paste(i_im, box, i_im)

            # 字符粘连
            delta_x += int(math.ceil(self.font_size*0.45)) 

        # 图形扭曲参数 
        params = [1 - float(random.randint(1, 2)) / 100, 
                  0, 
                  0, 
                  0, 
                  1 - float(random.randint(1, 10)) / 100, 
                  float(random.randint(1, 2)) / 500, 
                  0.001, 
                  float(random.randint(1, 2)) / 500 
                  ] 
        #im = im.transform((self.img_width, self.img_height), Image.PERSPECTIVE, params) 

        del draw
        buf = StringIO.StringIO()
        im.save(buf,'gif')
        buf.closed
        return HttpResponse(buf.getvalue(),'image/gif')

    def validate(self, code):
        """ 
        validate user's input
        """

        if not code:
            return False
        code = code.strip()
        _code = self.django_request.session.get(self.session_key) or ''
        self.django_request.session[self.session_key] = ''
        return _code.lower() == str(code).lower()

    def check(self,code):
        """
        This function will no longer be supported after  version  0.4
        """

        return self.validate(code)


class Code(Captcha):
    """
    compatibility for less than v2.0.6 
    """
    pass

if __name__ == '__main__':
    import mock
    request = mock.Mock()
    c = Captcha(request)

