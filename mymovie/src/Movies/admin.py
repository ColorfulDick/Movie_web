# -*- coding:utf-8 -*-
from Movies.models import *
import xadmin
# Register your models here.
class movieAdmin(object):
    list_display = ('moviename','relese_time', 'Type',)
    search_fields = ('moviename','relese_time', 'Type',)
    list_filter = ('moviename','relese_time', 'Type',)
    model_icon = 'fa fa-film' 
    
class movies_typeAdmin(object):
    list_display = ('type',)
    search_fields = ('type',)
    list_filter = ('type',)

class BannerAdmin(object):
    list_display = ('title','url','add_time',)
    search_fields = ('title','url','add_time',)
    list_filter = ('title','url','add_time',)
    
           
xadmin.site.register(movie, movieAdmin)
xadmin.site.register(movies_type,movies_typeAdmin)
xadmin.site.register(Banner,BannerAdmin)
xadmin.AdminSite.site_header ='电影管理'
xadmin.AdminSite.site_title = '电影管理列表'