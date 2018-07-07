from django.conf.urls import url
from django.contrib import admin

from userapp import views


urlpatterns = [
    # 声明注册请求
    url(r'^regist', views.regist),

    # 图片上传请求
    url(r'^upload', views.upload),

    # 用户登录请求
    url(r'^login', views.login),

    # 用户 注销
    url(r'^logout', views.logout)
]
