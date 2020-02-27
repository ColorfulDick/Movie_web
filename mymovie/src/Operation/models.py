#-*- coding:utf-8 -*-
from django.db import models
from Users.models import User#导入外键需要的表
from Movies.models import movie
# Create your models here.
class MovieComments(models.Model):
    '''影片评论'''
    user = models.ForeignKey(User,to_field='username',verbose_name='用户',on_delete=models.CASCADE)#这是一个外键，指向User表的username字段，下同
    movie = models.ForeignKey(movie, to_field='moviename',verbose_name='电影',on_delete=models.CASCADE)
    comments = models.TextField('评论',max_length=200)
    add_time = models.DateTimeField('添加时间', auto_now_add=True)

    class Meta:
        verbose_name = '影片评论'
        verbose_name_plural = verbose_name
        
        
class UserFavorite(models.Model):
    '''用户收藏'''
    user = models.ForeignKey(User, to_field='username',verbose_name='用户',on_delete=models.CASCADE)
    movie = models.ForeignKey(movie, to_field='moviename',verbose_name='电影',on_delete=models.CASCADE)
    add_time = models.DateTimeField('添加时间', auto_now_add=True)

    class Meta:
        verbose_name = '用户收藏'
        verbose_name_plural = verbose_name
        
class History_Operation(models.Model):
    '''用户历史浏览记录'''
    user = models.ForeignKey(User, to_field='username',verbose_name='用户',on_delete=models.CASCADE)
    movie = models.ForeignKey(movie, to_field='moviename',verbose_name='电影',on_delete=models.CASCADE)
    add_time = models.CharField(verbose_name='电影名称',max_length=16)
    
    class Meta:
        verbose_name = '浏览历史'
        verbose_name_plural = verbose_name