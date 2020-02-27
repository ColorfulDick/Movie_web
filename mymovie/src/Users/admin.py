# -*- coding:utf-8 -*-
#from django.contrib import admin
import xadmin#上面那行代码是启用django自带后台的，这里我们用xadmin的后台
from Users.models import *#导入models里所有类，将数据库与后台进行关联
from xadmin import views
# Register your models here.
class UserAdmin(object):
    list_display = ('username','gender', 'email','area','createDate','loadDate')#在后台显示的字段
    search_fields = ('username','gender', 'email','area','createDate','loadDate')#可以在后台用关键字搜索搜索到的字段
    list_filter = ('username','gender', 'email','area','createDate','loadDate')#可以批量过滤的字段，如筛选出地区和性别都一样的
    model_icon = 'fa fa-user' #配置在后台显示的图标
    
class EmailVerifyRecordAdmin(object):   
    list_display = ('code', 'email', 'send_type', 'send_time')   
    search_fields = ('code', 'email', 'send_type')   
    list_filter = ('code', 'email', 'send_type', 'send_time')
    model_icon = 'fa fa-envelope-o'

class BaseSetting(object):
    # 开启xadmin主题功能，这样可以选择不同色彩的后台主题
    enable_themes = True
    use_bootswatch = True

# 将基本配置管理与view绑定
xadmin.site.register(views.BaseAdminView,BaseSetting)#对我们的配置进行注册，这样我们才能在后台看到它们
xadmin.site.register(EmailVerifyRecord,EmailVerifyRecordAdmin)
xadmin.site.register(User, UserAdmin)
xadmin.AdminSite.site_header ='用户管理'#给列表入口进行命名
xadmin.AdminSite.site_title = '用户管理列表'