#-*- coding:utf-8 -*-
import datetime
# Create your views here.
from django.shortcuts import render,redirect#用于在函数结束后返回一个或几个变量给指定的页面
from django.http import HttpResponse,Http404,HttpResponseRedirect #django的http通信模块，主要用于前后端通信，每个views.py都会用到
from Users.models import User,ForgetForm,ResetForm,EmailVerifyRecord 
from django.contrib.auth.hashers import make_password,check_password #加密模块，用于加密密码
from django.views import View #视图模块，用于在不发送请求的情况下调用含有这个参数的函数
from django.contrib import messages
from PIL import Image, ImageDraw, ImageFont#此为Python的一个第三方包，主要用来绘画验证码
import random,os
from Movies import views
from django.core.mail import send_mail #用来发送改密钥匙的邮箱验证码
from mymovie.settings import EMAIL_FROM#获取在setting配置的邮箱信息
from io import BytesIO
from random import Random
import uuid 
# Django的form的作用：
# 1、生成html标签
# 2、用来做用户提交的验证
# Form的验证思路
# 前端：form表单
# 后台：创建form类，当请求到来时，先匹配，匹配出正确和错误信息。
def get_ip(request):#获取用户的登录ip的函数
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]#所以这里是真实的ip
    else:
        ip = request.META.get('REMOTE_ADDR')#这里获得代理ip
    return ip

     
def regist(request):#注册用的函数
    if request.method == 'GET':
        return render(request, 'regist.html')
    if request.method == 'POST': 
        username = request.POST['username']#通过POST方法获得用户填写的各种信息
        gender = request.POST.get('gender')
        password = request.POST['password']
        repassword = request.POST['repassword']
        email = request.POST['email']
        userip= get_ip(request)
        valid_code = request.POST.get("valid_code")  # 获取用户填写的验证码
        if valid_code and valid_code.upper() == request.session.get("valid_code", "").upper() and valid_code!='':#比对验证码
            if password!=repassword:
                messages.success(request,"两次密码不一致，请重新输入")
                return render(request,'regist.html',{'valid_code':'两次密码不一致，请重新输入'})
            else:  
                if User.objects.filter(username=username,email=email).exists() or username=='':
                    messages.success(request,"您已经注册过了，请直接登录")
                    return render(request,'regist.html',{'valid_code':'您已经注册过了,请直接登录'})
                else:
                    password = make_password(password)#对密码进行加密
                    User.objects.create(username=username, gender=gender,password=password,email=email,userip=userip)
                    messages.success(request,"注册成功！请直接登录吧")
                    return render(request,'login.html',{'valid_code':'注册成功!清直接登录吧'})#注册成功，跳转至登录页并弹窗提醒
        else:
            messages.success(request,"验证码错误，请重新填写")#如果验证码不正确，弹窗提醒
            return render(request,'regist.html',{'valid_code':'验证码错误，请重新填写'})
        
def login(request):#登录功能
    if request.method == 'GET':
        request.session['login_from'] = request.META.get('HTTP_REFERER', '/')#记录用户得上一个访问得页面
        return render(request, 'login.html')
         
    if request.method == 'POST':     
        # 如果登录成功，绑定参数到cookie中，set_cookie     
        username = request.POST['username']     
        password = request.POST['password']
        nowtime=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')#获取登录时间
        ip=get_ip(request)
        valid_code = request.POST.get("valid_code")  # 获取用户填写的验证码
        if valid_code and valid_code.upper() == request.session.get("valid_code", "").upper() and valid_code!='':     
            # 查询用户是否在数据库中    
            if User.objects.filter(username=username).exists():       
                user = User.objects.get(username=username)
                if check_password(password, user.password):# 验证密码                    
                    User.objects.filter(username=username).update(loadDate=nowtime,userip=ip)         
                    response = HttpResponseRedirect('/index/')         #max_age 存活时间(秒)         
                    response.set_cookie('username', username, max_age=10000)   # 存在客户端
                    request.session['username'] = username     #存在服务端 
                    #messages.success(request,"登录成功")           
                    return HttpResponseRedirect(request.session['login_from']) #返回用户登录前的页面      
                else:
                    messages.success(request,"用户密码错误，请重新填写")         #弹窗提示('用户密码错误')         
                    return render(request, 'login.html', {'password': '用户密码错误'})     
            else:
                messages.success(request,"用户不存在")       # return HttpResponse('用户不存在')       
                return render(request, 'login.html', {'username': '用户不存在'}) 
        else:
            messages.success(request,"验证码错误，请重新填写")
            return render(request,'login.html',{'valid_code':'验证码错误，请重新填写'})

  
def logout(request):  #登出功能
    if request.method == 'GET':     
        response = HttpResponseRedirect('/')
        response.delete_cookie("username")#删除cookie
        request.session.flush()#删除所有session        
        return response

def usercenter(request):#用户中心
    if request.method == 'GET': 
        username = request.session.get('username', '')     
        if not username:       
            return HttpResponseRedirect('/login/')
        name = User.objects.get(username=username)
        return render(request, 'user.html', {'name': name})

import uuid,hashlib
def get_unique_str():
    uuid_str = str(uuid.uuid4())
    md5 = hashlib.md5()
    md5.update(uuid_str.encode('utf-8'))
    return md5.hexdigest()

def heads(request):#上传头像的函数
    if request.method == 'POST':
        avatar_img = request.FILES.get("image")
        username = request.session.get('username', '')
        name = User.objects.get(username=username)
        '''
        #帮助自己了解InMemoryUploadedFile对象的代码
        print(avatar_img)
        print(avatar_img.file,avatar_img.field_name,avatar_img.name,avatar_img.content_type,avatar_img.size,avatar_img.charset,avatar_img.content_type_extra)
        '''
        name.photo=avatar_img
        name.save()
        return HttpResponse("上传成功")

def get_valid_img(request):  #调用Pillow模块绘制验证码，其实用captcha也可以的,所以本项目用了两种方式生成验证码，主要是为了安全，防止生成验证码的规律被掌握
    # 获取随机颜色的函数
    def get_random_color():
        return random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)

    # 生成一个图片对象
    img_obj = Image.new(
        'RGB',
        (220, 35),
        get_random_color()
    )
    # 在生成的图片上写字符
    # 生成一个图片画笔对象
    draw_obj = ImageDraw.Draw(img_obj)
    # 加载字体文件， 得到一个字体对象
    font_obj = ImageFont.truetype("/static/font/ARLRDBD.TTF", 40)
    # 开始生成随机字符串并且写到图片上
    tmp_list = []
    for i in range(5):
        u = chr(random.randint(65, 90))  # 生成大写字母
        l = chr(random.randint(97, 122))  # 生成小写字母
        n = str(random.randint(0, 9))  # 生成数字，注意要转换成字符串类型

        tmp = random.choice([u, l, n])
        tmp_list.append(tmp)
        draw_obj.text((20 + 40 * i, 0), tmp, fill=get_random_color(), font=font_obj)

    # 保存到session
    request.session["valid_code"] = "".join(tmp_list)
    # 加干扰线
    width = 220  # 图片宽度（防止越界）
    height = 35
    for i in range(5):
        x1 = random.randint(0, width)
        x2 = random.randint(0, width)
        y1 = random.randint(0, height)
        y2 = random.randint(0, height)
        draw_obj.line((x1, y1, x2, y2), fill=get_random_color())

    # 加干扰点
    for i in range(40):
        draw_obj.point((random.randint(0, width), random.randint(0, height)), fill=get_random_color())
        x = random.randint(0, width)
        y = random.randint(0, height)
        draw_obj.arc((x, y, x+4, y+4), 0, 90, fill=get_random_color())

    # 不需要在硬盘上保存文件，直接在内存中加载就可以
    io_obj = BytesIO()
    # 将生成的图片数据保存在io对象中
    img_obj.save(io_obj, "png")
    # 从io对象里面取上一步保存的数据
    data = io_obj.getvalue()
    return HttpResponse(data)

def random_str(random_length=8):   #用于生成随机字符串，用户的验证码将在这里取得
    str=''   
    chars='AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'  
    length=len(chars)-1  
    random=Random()   
    for i in range(random_length):     
        str+=chars[random.randint(0,length)]   
    return str  
def send_register_email(email,send_type):   
    email_record=EmailVerifyRecord()         #用于生成随机验证码和对应的邮箱并存入数据库中，将验证码以链接形式发送至邮箱，点击进行激活
    code=random_str(16)              #将随机验证码和用户对应的邮箱存在一起，以验证用户
    email_record.code=code   
    email_record.email=email   
    email_record.send_type=send_type   
    email_record.save()     
    email_title=''   
    email_body=''     
    if send_type=='forget':     
        email_title = '选课系统密码重置链接'    
        email_body = '请点击下面的链接重置你的密码：http://127.0.0.1:8000/reset/{0}'.format(code)  #把生成的随机字符串拼接在地址http://127.0.0.1:8000/reset/后面     
        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])     #将对应的验证码发给对应的用户
        if send_status:       
            pass 

class ForgetPwdView(View):  
    '''忘记密码'''    
    def get(self,request):
        forget_form=ForgetForm()
        return render(request,'forget.html',{'forget_form':forget_form})
    def post(self,request):     
        forget_form = ForgetForm(request.POST)     
        if forget_form.is_valid():       
            email=request.POST.get('email','')       
            send_register_email(email,'forget')       
            return render(request,'success_send.html')     
        else:       
            return render(request,'forget.html',{'forget_form':forget_form})
             
class ResetView(View):   
    '''重置密码'''  
    def get(self,request,active_code):     
        record=EmailVerifyRecord.objects.filter(code=active_code)     
        print(record)     
        if record:       
            for i in record:         
                email=i.email         
                is_register=User.objects.filter(email=email)         
                if is_register:           
                    return render(request,'pwd_reset.html',{'email':email})     
        return redirect('index')     
                    #因为<form>表单中的路径要是确定的，所以post函数另外定义一个类来完成 
class ModifyView(View):   
    """重置密码post部分"""  
    def post(self,request):     #主要判断两次密码输入是否一致
        reset_form=ResetForm(request.POST)     
        if reset_form.is_valid():       
            pwd1=request.POST.get('newpwd1','')       
            pwd2=request.POST.get('newpwd2','')       
            email=request.POST.get('email','')       
            if pwd1!=pwd2:         
                return render(request,'pwd_reset.html',{'msg':'密码不一致！'})       
            else:         
                user=User.objects.get(email=email)         
                user.password=make_password(pwd2)         
                user.save()         
                return redirect('index')     
        else:       
            email=request.POST.get('email','')       
            return render(request,'pwd_reset.html',{'msg':reset_form.errors}) 
            
def user_change(request):
    user = request.GET['nick_name']
    gender = request.GET['gender']
    area = request.GET['adress']
    User.objects.filter(username=user).update(gender=gender,area=area)     
    return render(request,'usercenter.html',)