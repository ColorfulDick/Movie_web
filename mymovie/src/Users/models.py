#-*- coding:utf-8 -*-
from django.db import models #定义数据库模型的总模块，里面有很多方法可以用
from captcha.fields import CaptchaField #一个验证码模块，需要用pip3另外安装
from django import forms #表单模块，用来验证用户提交的信息，比如用户重置密码时填写的邮箱
import datetime #时间模块，用于记录用户的注册、登录时间
import os #系统模块，用于编写静态路由机制函数
import uuid,hashlib
def get_unique_str():#用来给图片生成唯一id
    uuid_str = str(uuid.uuid4())
    md5 = hashlib.md5()
    md5.update(uuid_str.encode('utf-8'))
    return md5.hexdigest()
    
class User(models.Model):
    """用户表"""
    gender_choices=(#定义一个单选模块给负责记录性别的gender模块使用
        ('男', '男'),
        ('女','女'),
        )
    username = models.CharField(verbose_name='用户名',max_length=20,unique=True)#创建一个字符字段，长度为20，且是唯一的
    password = models.CharField(verbose_name='密码',max_length=100)
    gender = models.CharField(verbose_name='性别',choices=gender_choices,max_length=1)
    email = models.EmailField(verbose_name='邮箱',default='')#邮箱字段，自动验证地址合法性，不需要验证max_length
    area = models.CharField(verbose_name='地区',max_length=15)
    createDate = models.DateTimeField('创建该账号的时间',auto_now_add=True)#时间字段，用于存储一个详细的时间，会在表生成的时候自动生成
    loadDate = models.DateTimeField('上次登录时间',auto_now=True)#时间字段，会在表更新的时候自动更新该时间
    userip = models.GenericIPAddressField('用户登录ip',protocol="both")
    '''
    def get_photo(self, filename):#上传用户头像的函数，除了指定上传路径，还可以改变源文件的名称再上传，防止撞名
        return os.path.join('photo', '%s_%s_%s_%s' % (self.username, self.gender, self.email, os.path.splitext(filename)[1]))
    '''
    def get_photo(self,filename):#我重写了一个get_photo函数，这样可以为每张图片生成唯一id，更加贴近生产环境
        filename=get_unique_str()+'.'+filename.split('.')[-1]
        return os.path.join('photo/',filename)
    photo = models.ImageField(verbose_name='头像', upload_to=get_photo, blank=True, null=True)
    
    class Meta:#定义该表在后台显示的名称，下面那个函数功能类似
        verbose_name = '用户列表'
        verbose_name_plural = verbose_name
        
    def __str__(self):  
        return self.username    


class EmailVerifyRecord(models.Model):   
    """邮箱激活码，将用于找回密码"""  
    code=models.CharField(max_length=20,verbose_name='验证码')   
    email=models.EmailField(max_length=50,verbose_name='邮箱')   
    send_type=models.CharField(verbose_name='验证码类型',choices=(('register','注册'),('forget','忘记密码')), max_length=20)   
    send_time=models.DateTimeField(verbose_name='发送时间',default=datetime.datetime.now())   
    class Meta:     
        verbose_name='邮箱验证码'    
        verbose_name_plural=verbose_name
    def __str__(self):     
        return '{0}({1})'.format(self.code,self.email)
    
class ForgetForm(forms.Form):   #用于暂存用户邮箱，会在用户重置密码时用到
    email=forms.EmailField(required=True)   
    captcha=CaptchaField(error_messages={'invalid':'验证码错误'})   #reset.html中，用于验证新设的密码长度是否达标 
class ResetForm(forms.Form):   #用于临时放用户的重置密码，后面会用到
    newpwd1=forms.CharField(required=True,min_length=6,error_messages={'required': '密码不能为空.', 'min_length': "至少6位"})   
    newpwd2 = forms.CharField(required=True, min_length=6, error_messages={'required': '密码不能为空.', 'min_length': "至少6位"})     
    