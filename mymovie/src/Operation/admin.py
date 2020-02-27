# -*- coding:utf-8 -*-
from django.contrib import admin
from Operation.models import *
import xadmin
# Register your models here.
class MovieCommentsAdmin(object):
    list_display = ('user','movie','add_time')
    search_fields = ('user','movie','add_time')
    list_filter = ('user','movie','add_time')
    model_icon = 'fa fa-comments' 
class UserFavoriteAdmin(object):
    list_display = ('user','movie','add_time')
    search_fields = ('user','movie','add_time')
    list_filter = ('user','movie','add_time')
    model_icon = 'fa fa-star-o' 
    
class History_OperationAdmin(object):
    list_display = ('user','movie','add_time')
    search_fields = ('user','movie','add_time')
    list_filter = ('user','movie','add_time')
    model_icon = 'fa fa-history'     

xadmin.site.register(MovieComments, MovieCommentsAdmin)    
xadmin.site.register(UserFavorite,UserFavoriteAdmin)
xadmin.site.register(History_Operation,History_OperationAdmin)
xadmin.AdminSite.site_header ='电影管理'
xadmin.AdminSite.site_title = '电影管理列表'