import os
import uuid

from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from XSproject import settings
from userapp.forms import UserForm
from userapp.models import UserProfile
from json import loads


# Create your views here.
def regist(request):
    if request.method == 'GET':
        return render(request, 'user/regist.html')
    else: # post
        # user = UserProfile()
        # user.username = request.POST.get('username')
        # user.password = request.POST.get('password')
        # user.phone = request.POST.get('phone')
        # user.photo = request.FILES.get('photo')

        # 创建UserForm的实例对象
        # 要求：表单中指定的字段名必须和model模型中字段名保持一致
        userForm = UserForm(request.POST)

        # 保存之前要验证数据
        if userForm.is_valid():  # 验证通过
            userForm.save()
            return redirect('/art/')
        else:
            print('验证出错：', userForm.errors.as_json())

            # form.errors.as_json() 返回是 json字符串
            # 格式： {'字段名1':[{'message':'xx', code:'required'}],
            #        '字段名2':[{'message':'xx', code:'required'}]}
            return render(request, 'user/regist.html',
                          {'errors': loads(userForm.errors.as_json())})


@csrf_exempt  # 不验证csrf的token
def upload(request):
    # 实现图片文件上传的功能(接口)
    # 请求方法： POST
    # 请求参数： photo 文件类型

    # 实现功能
    # 1. 获取上传文件对象
    uploadFile = request.FILES.get('photo')
    print(uploadFile)

    # 2. 配置文件保存的路径和文件名
    imgDir = os.path.join(settings.MEDIA_ROOT, 'users')
    imgFileName = str(uuid.uuid4()).replace('-', '') + '.' + uploadFile.name.split('.')[-1]

    # 3.开始将上传文件内容写入到服务器中
    with open(os.path.join(imgDir, imgFileName), 'wb') as f:
        for chunk in uploadFile.chunks():
            f.write(chunk)

    print('文件上传成功...!')

    # 响应的数据：
    # '{"status":"ok","path": "images/xxx.jpg"}'
    return JsonResponse({'status': 'ok',
                         'path': 'users/'+imgFileName})


def login(request):
    errors = []
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # 1. 根据用户名查找用户信息
        rs = UserProfile.objects.filter(username=username)
        if not rs.exists():
            errors.append(username+' 用户不存在')
        else:
            user:UserProfile = rs.first()  # 从查询结果中读取第一个记录（对象 ）
            if not user.varify_passwd(password):
                # 密码不一样
                errors.append('口令错误，请重试！')
            else:
                # 登录成功
                # 向session中写入 user唯一标识
                request.session['user_id'] = user.id

                return redirect('/art/')

    # 用户登录
    return render(request,
                  'user/login.html',
                  {'errors': errors})


def logout(request):
    # 清除session
    request.session.flush()

    return redirect('/art/')