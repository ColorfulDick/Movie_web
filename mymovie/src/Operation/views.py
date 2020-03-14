#-*- coding:utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse,Http404,HttpResponseRedirect
from Operation.models import UserFavorite,MovieComments,History_Operation
from django.views import View
from Movies.models import movie
from Users.models import User
from django.contrib import messages
import datetime
from django.core.cache import cache
import collections
import time
# Create your views here.

def collect(request):#该函数用于显示用户收藏的电影
    if request.method == 'GET':
        username = request.session.get('username', '')
        if not username:       
            return HttpResponseRedirect('/login/')
        name = User.objects.get(username=username)
        collectmovies=UserFavorite.objects.filter(user=username)
        return render(request,'mycollect.html',{'collectmovies':collectmovies,'name':name,})

def fav(request):#该函数用于响应用户的收藏电影请求，与js函数配合使用
    has_fav=request.GET['has_fav']#获得js传过来的has_fav值
    getMovieName = request.GET['moviename']
    username = request.session.get('username', '')
    user=User.objects.get(username=username)
    movie_name=movie.objects.get(moviename=getMovieName)#外键的更新需要影片的对象，所以要先获得影片的对象
    if has_fav=="true":
        if UserFavorite.objects.filter(user=user,movie=movie_name).exists():
            movie.objects.filter(moviename=getMovieName).update(collect=movie_name.collect-1)
            UserFavorite.objects.filter(user=username,movie=getMovieName).delete()
            messages.success(request,username+"取消收藏"+getMovieName+"成功")#告诉后台谁取消收藏了什么电影
            n="取消收藏成功"
            return HttpResponse(n)        
    movie.objects.filter(moviename=getMovieName).update(collect=movie_name.collect+1)#收藏的人多了一个，+1    
    nowtime=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')#获取收藏时间，  
    u=UserFavorite(user=user,movie=movie_name,add_time=nowtime)
    u.save()    
    messages.success(request,username+"收藏"+getMovieName+"成功")
    n="收藏成功"
    return HttpResponse(n)
    
def comments(request):
    comment=request.GET['comment']#获得js传过来的评论comment的值
    getMovieName = request.GET['moviename']
    username = request.session.get('username', '')
    user=User.objects.get(username=username)
    movie_name=movie.objects.get(moviename=getMovieName)#
    c=MovieComments(user=user,movie=movie_name,comments=comment,add_time=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    c.save()
    r="评论成功"
    return HttpResponse(r)
    
def history(username,video):
    user_history_broswing=cache.get(username)#从redis缓存里找用户的操作记录
    name=User.objects.get(username=username)
    if user_history_broswing == None:#如果没有就从数据库里找
        intermediate=History_Operation.objects.filter(user=username)
        if intermediate == None:#数据库里也没有就弄个新的队列放进redis里来操作
            user_history_broswing=[]
            video.add_time=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            user_history_broswing.append(video)
            cache.set(username,user_history_broswing)
            time.sleep(5)
            History_Operation.objects.create(user=name,movie=video,add_time=video.add_time)
            return 0   
        user_history_broswing=[]
        for i in intermediate:
            j=i.movie
            j.add_time=i.add_time
            user_history_broswing.append(j)
        if video in user_history_broswing:
            user_history_broswing.remove(video)
        video.add_time=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')#给用户点击过的影片对象加个“浏览时间”属性然后塞进队列里
        user_history_broswing.append(video)
        cache.set(username,user_history_broswing)
        time.sleep(10)#如果10s内无人操作，则进行缓存落地，将redis内的内容塞进永久性数据库里
        for i in user_history_broswing:
            if History_Operation.objects.filter(user=name,movie=i).exists() == True:#看看数据库里有没有redis里的这条记录
                History_Operation.objects.filter(user=name,movie=i).update(add_time=i.add_time)#如果有，更新一下时间就ok
            else:
                History_Operation.objects.create(user=name,movie=i,add_time=i.add_time)#如果没有，就直接创建一个；浏览记录 
        return 0        
    if video in user_history_broswing:
            user_history_broswing.remove(video)       
    video.add_time=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    user_history_broswing.append(video)
    cache.set(username,user_history_broswing)
    time.sleep(10)#如果10s内无人操作，则进行缓存落地，将redis内的内容塞进永久性数据库里
    for i in user_history_broswing:
        if History_Operation.objects.filter(user=name,movie=i).exists() == True:#看看数据库里有没有redis里的这条记录
            History_Operation.objects.filter(user=name,movie=i).update(add_time=i.add_time)#如果有，更新一下时间就ok
        else:
            History_Operation.objects.create(user=name,movie=i,add_time=i.add_time)#如果没有，就直接创建一个；浏览记录 
    return 0
    
def browsing_history(request):
    if request.method == 'GET':
        username = request.session.get('username')
        name=User.objects.get(username=username)
        user_history_broswing=cache.get(username)
        if user_history_broswing==None:#如果redis里没有该用户的操作记录，就从数据库里找
            intermediate=History_Operation.objects.filter(user=username)
            user_history_broswing=[]
            for i in intermediate:#为每个movie对象添加它本来没有的add_time属性(movie是add_time属性在外键History_Operation里才有)
                j=i.movie
                j.add_time=i.add_time
                user_history_broswing.append(j)
            user_history_broswing.reverse()
            return render(request,'browsing_history.html',{'user_history_broswing':user_history_broswing,'name':name})
        user_history_broswing.reverse()    
        return render(request,'browsing_history.html',{'user_history_broswing':user_history_broswing,'name':name})