from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from artapp.models import ArtTag, Art
from userapp.models import UserProfile


def index(requset):
    # 获取请求参数中的tag标签分类的id
    tag_id = requset.GET.get('tag')
    pageNum = requset.GET.get('page')

    if not pageNum:
        pageNum = 1  # 从第一页开始

    # 如果tag_id 不存在时，则表示为所有（即不分类型）
    if (not tag_id) or (tag_id == '0'):
        # 查询所有文章
        arts = Art.objects.all()
        tag_id = 0
    else:
        arts = Art.objects.filter(tag_id=tag_id).all()

    # 分页器Paginator
    paginator = Paginator(arts, 4)

    # 获取第 pageNum页
    # 判断当前的页码是否大于最大页数
    if int(pageNum) > paginator.num_pages:
        pageNum = paginator.num_pages
    elif int(pageNum) <= 0:  # 判断页码是否小于等于0
        pageNum = 1
    page = paginator.page(pageNum)

    # 从session中读取user_id，获取当前的登录的用户信息
    user_id = requset.session.get('user_id')
    user = None
    if user_id:
        user = UserProfile.objects.get(id=user_id)

    # 返回渲染模板
    return render(requset, 'art/list.html',
                  context={'arts': page.object_list,
                           'page_range': paginator.page_range,
                           'page': page,
                           'tag_id': int(tag_id),
                           'tags': ArtTag.objects.all(),
                           'user': user})


def add_tags(request):
    # 添加标签类型的处理函数
    if request.method == 'GET':
        # 新增, 修改
        # 判断是否为修改
        id = request.GET.get('id')
        tag = None
        if id:
            # 存在id,即为修改
            tag = ArtTag.objects.get(id=id)
        return render(request, 'art/edit_tags.html', {'tag': tag})
    else:
        # POST 请求
        # 新增, 修改
        if request.POST.get('id'):
            tag = ArtTag.objects.get(id=request.POST.get('id'))
        else:
            tag = ArtTag()
        tag.title = request.POST.get('title')
        tag.save()  # 保存到数据库

        return redirect('/art/list_tags')  # 重定向

def delete_tag(request):
    id = request.GET.get('id')
    if id:
        result = ArtTag.objects.filter(id=id)
        if result.exists():
            result.delete()

    # 重定向到列表页面
    return redirect('/art/list_tags')


def list_tags(request):
    return render(request,
                  'art/tags_list.html',
                  context={
                    'tags':   ArtTag.objects.all()
                  })