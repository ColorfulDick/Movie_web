#-*- coding:utf-8 -*-
from django.db import models
import os
# Create your models here.
class movies_type(models.Model):
    '''用于定义电影类型'''
    type=models.CharField(verbose_name='视频类型',max_length=10,unique=True)
    
    class Meta:
        verbose_name = '视频类型'
        verbose_name_plural = verbose_name
        
    def __str__(self):  
        return self.type

class movie(models.Model):
    '''电影'''
    moviename=models.CharField(verbose_name='电影名称',max_length=30,unique=True)
    presentation=models.TextField(verbose_name='内容介绍',max_length=300)
    relese_time=models.DateTimeField(verbose_name='发布时间',auto_now_add=True)
    click=models.IntegerField(verbose_name='点击率',default='0')
    Type=models.ManyToManyField(movies_type,verbose_name='视频类型',blank=True,related_name='movietype')
    collect=models.IntegerField(verbose_name='收藏人数',default='0')
    def get_cover(self, filename):#这个函数用于封面的上传
        return os.path.join('cover', '%s_%s_%s' % (self.moviename, self.relese_time, os.path.splitext(filename)[1]))
    cover = models.ImageField(verbose_name='封面', upload_to=get_cover, blank=True, null=True)
    def get_movie(self, filename):#这个函数用于视频的上传
        return os.path.join('movie', '%s_%s_%s' % (self.moviename, self.relese_time, os.path.splitext(filename)[1]))
    video = models.FileField(max_length=200,upload_to=get_movie, default='videos/default.mp4', blank=True,verbose_name='视频文件')#文件字段，可以上传一个任意文件，，这里设置默认为.mp4文件
    
    class Meta:
        verbose_name = '电影列表'
        verbose_name_plural = verbose_name
        
    def __str__(self):  
        return self.moviename
        
        
class Banner(models.Model):
    '''轮播图'''
    title = models.CharField('标题',max_length=100)
    image = models.ImageField(verbose_name='轮播图',upload_to='banner')
    url = models.URLField(verbose_name='访问地址',max_length=200)
    add_time = models.DateTimeField('添加时间',auto_now_add=True)

    class Meta:
        verbose_name = '轮播图'
        verbose_name_plural = verbose_name