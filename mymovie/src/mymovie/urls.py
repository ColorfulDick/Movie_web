"""mymovie URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from Users import views
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from Users.views import ForgetPwdView,ResetView,ModifyView
import xadmin
import Operation.views
import Movies.views,Users.views


urlpatterns = [
    path('silk/',include('silk.urls', namespace='silk')),
    path('admin/',xadmin.site.urls),#��̨��·��    
    path('regist/',views.regist),#ע���·��
    path('login/',views.login),#��¼��·��
    path('logout/',views.logout),#�ǳ���·��
    path('get_valid_img.png/', views.get_valid_img), #����������֤��ĺ���
    path('mycollect/',Operation.views.collect),    
    path('usercenter/',views.usercenter),
    path('',Movies.views.index,name='index'),
    path('search/',Movies.views.search),
    path('video/', Movies.views.video),
    path('forget/',ForgetPwdView.as_view(),name='forget_pwd'),   #�����ܱ��ʼ��ĺ���  
    path('reset/<str:active_code>',ResetView.as_view(),name='reset'),   #��������ĺ���
    path('modify/',ModifyView.as_view(),name='modify'), #���������post����
    path('captcha/',include('captcha.urls')), #��֤�벿�֣����������captcha
    path('fav/',Operation.views.fav),
    path('comments/',Operation.views.comments),
    path('image_upload/',Users.views.heads),
    path('page/',Movies.views.page),
    path('user_change/',Users.views.user_change),
    path('broswing_history/',Operation.views.browsing_history)
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
