from django.conf.urls import url
from django.contrib import admin
from artapp.views import *
from artapp import views_art


urlpatterns = [
    # 声明主页面的请求
    url(r'^tags$', add_tags),
    url(r'^list_tags', list_tags),
    url(r'^delete_tag', delete_tag),
    url(r'^art_edit', views_art.art_edit),  # 编辑文章
    url(r'^search', views_art.search),  # 搜索文章
    url(r'^show', views_art.show),
    url(r'^', index),

]
