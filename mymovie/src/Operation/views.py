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
from django_redis import get_redis_connection
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
            #messages.success(request,username+"取消收藏"+getMovieName+"成功")#告诉后台谁取消收藏了什么电影
            n="取消收藏成功"
            return HttpResponse(n)        
    movie.objects.filter(moviename=getMovieName).update(collect=movie_name.collect+1)#收藏的人多了一个，+1    
    nowtime=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')#获取收藏时间，  
    u=UserFavorite(user=user,movie=movie_name,add_time=nowtime)
    u.save()    
    #messages.success(request,username+"收藏"+getMovieName+"成功")
    n="收藏成功"
    return HttpResponse(n)
    
def comments(request):
    comment=request.GET['comment']#获得js传过来的评论comment的值
    getMovieName = request.GET['moviename']
    username = request.session.get('username', '')
    user=User.objects.get(username=username)
    movie_name=movie.objects.get(moviename=getMovieName)
    c=MovieComments(user=user,movie=movie_name,comments=comment,add_time=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    c.save()
    r="评论成功"
    return HttpResponse(r)

def history(username,video):
	conn = get_redis_connection('default')#设置redis连接池
	if conn.exists(username) == False:#从redis缓存里找用户的操作记录,如果没有就直接存进redis里
		add_time=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
		conn.hset(username,video.id,add_time)
		time.sleep(5)#5s后无操作，则将redis的数据永久备份至数据库中
		name=User.objects.get(username=username)
		History_Operation.objects.create(user=name,movie=video,add_time=add_time)
		return 0
	db_date=History_Operation.objects.filter(user=username)
	for i in db_date:#将数据库内的数据同步到redis中
		conn.hset(i.user.username,i.movie.id,i.add_time)
	add_time=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	conn.hset(username,video.id,add_time)
	time.sleep(5)
	mov=movie.objects.get(id=video.id)
	name=User.objects.get(username=username)
	add_time=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	if History_Operation.objects.filter(user=name,movie=video).exists() == True:#看看数据库里有没有redis里的这条记录
		History_Operation.objects.filter(user=name,movie=video).update(add_time=add_time)#如果有，更新一下时间就ok
	else:
		History_Operation.objects.create(user=name,movie=video,add_time=add_time)#如果没有，就直接创建一个；浏览记录 
	return 0

class History_Operations:#设置一个对象用来存放movie对象和用户的操作时间（模拟History_Operation对象再传给前端）
	def __init__(self,movie,add_time):
		self.movie=movie
		self.add_time=add_time
		
def browsing_history(request):
	if request.method == 'GET':
		username = request.session.get('username')
		name=User.objects.get(username=username)
		conn = get_redis_connection('default')#设置redis连接池
		history_broswing=conn.hgetall(username)		
		if history_broswing== None:
			user_history_broswing=History_Operation.objects.filter(user=name).order_by('-add_time')
			return render(request,'browsing_history.html',{'user_history_broswing':user_history_broswing,'name':name})
		user_history_broswing=[]
		for i,j in history_broswing.items():
			mov=movie.objects.get(id=str(i,encoding='utf-8'))
			intermediate=History_Operations(mov,str(j,encoding='utf-8'))
			user_history_broswing.append(intermediate)
		user_history_broswing.sort(key=lambda x:x.add_time, reverse=True)
		return render(request,'browsing_history.html',{'user_history_broswing':user_history_broswing,'name':name})
