#-*- coding:utf-8 -*-
from django.test import TestCase

# Create your tests here.
from silk.profiling.profiler import silk_profile

@silk_profile(name='user login') # name在Profiling页面区分不同请求名称
def test(request):
    pass