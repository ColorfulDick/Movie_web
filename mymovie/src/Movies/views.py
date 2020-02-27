#-*- coding:utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse,Http404,HttpResponseRedirect
from Movies.models import movie,Banner
from Users.models import User
from Operation.models import UserFavorite,MovieComments
from django.views import View
from Operation.views import history
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger#django的分页器，用于评论分页功能
from multiprocessing import Process
import threading

# Create your views here.
def index(request):
    if request.method == 'GET':         
        username = request.session.get('username')
        all_banners=Banner.objects.all()
        newest=movie.objects.all().order_by('-relese_time')[:15]#开始调出最新的片子，并把最新的15条赋值给一个变量
        most_click=movie.objects.all().order_by('-click')[:5]     
        if not username:       
            #如果没登录，就只推荐最新的电影给他
            return render(request,'index.html',{'newest':newest,'all_banners':all_banners,'most_click':most_click})
        #如果有用户登录
        usercollect=UserFavorite.objects.filter(user=username)
        person=UserFavorite.objects.none()
        for i in usercollect:
            collectusers=UserFavorite.objects.filter(movie=i.movie).exclude(user=username)
            person=person|collectusers
        rec=UserFavorite.objects.none()
        for i in person:
            a=UserFavorite.objects.filter(user=i.user).exclude(movie=i.movie)
            rec=rec|a
        recommend=[]
        for i in rec:
            a=movie.objects.get(moviename=i.movie)
            recommend.append(a)   
        name = User.objects.get(username=username)
        return render(request, 'index.html', {'name': name,'newest':newest,'recommend':recommend,'all_banners':all_banners,'most_click':most_click})


def search(request):
    if request.method =='GET':
        username = request.session.get('username')
        if not username:
            return HttpResponseRedirect('/login/')
        name = User.objects.get(username=username)
        getSearch = request.GET.get('keywords')
        if movie.objects.filter(moviename__icontains=getSearch).exists():
            result=movie.objects.filter(moviename__icontains=getSearch)
            return render(request,'search.html',{'result':result,'name':name})
        else:
            return HttpResponse('很抱歉，没有找到')
    
  
def video(request):#该函数用于渲染电影播放界面
     if request.method == 'GET':         
        username = request.session.get('username')
        has_fav = "收藏"    #如果用户没登录，页面默认为没有收藏 
        getMovieName = request.GET.get('moviename')#获取url传过来的参数，里面有电影名称
        video=movie.objects.get(moviename=getMovieName)#找到被点击的影片对象，并以列表的形式放在一个变量里传给前端
        comments_list=MovieComments.objects.filter(movie=getMovieName)#获取影片的评论
        paginator=Paginator(comments_list,3)#实例化结果集，每页5条数据，少于3条则合并到上一页
        page=1        
        try:
            customer=paginator.page(page)
        except PageNotAnInteger:
            customer=paginator.page(1)
        except EmptyPage:
            customer=paginator.page(paginator.num_pages)
        movie.objects.filter(moviename=getMovieName).update(click=video.click+1)#有人点击了这部影片,点击率+1
        #下面是同类推荐算法
        list=[]
        for a in video.Type.filter().all():  #找到这个影片的所有类型的id，并通过类型的id找到具备这些类型的电影
            for b in movie.objects.filter(Type=a.id):#通过id找到指定的电影
               list.append(b)#申请一个名为list的列表，用append函数将得到的影片对象收集进这个列表中
               recommend=set(list)#利用set函数去掉重复的movie对象
        recommend.remove(video)#在推荐中去掉被点击的影片   
        if not username:  #如果用户没有登录，就不会显示已经被收藏，也不会记录用户的历史操作     
            return render(request,'video.html',{'video':video,'recommend':recommend,'has_fav':has_fav,'customer':customer})
        name = User.objects.get(username=username)
        if UserFavorite.objects.filter(user=username, movie=getMovieName):#判断收藏状态
            has_fav = "取消收藏"            #如果有收藏，则显示他收藏了
        t=threading.Thread(target=history,args=(username,video))#开启一个线程，记录用户看过的影片，
        t.start()
        return render(request, 'video.html', {'name': name,'video':video,'recommend':recommend,'has_fav':has_fav,'customer':customer})

def page(request):#用于评论区翻页的函数，配合ajax可以局部刷新评论区
    getMovieName = request.GET['moviename']
    page = request.GET['page']
    comments_list=MovieComments.objects.filter(movie=getMovieName)#获取影片的评论
    paginator=Paginator(comments_list,3)#实例化结果集，每页5条数据，少于3条则合并到上一页       
    try:
        customer=paginator.page(page)
    except PageNotAnInteger:
        customer=paginator.page(1)
    except EmptyPage:
        customer=paginator.page(paginator.num_pages)
    return render(request, 'comments.html', {'customer':customer})