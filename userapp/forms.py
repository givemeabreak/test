from django import forms
from django.core.exceptions import ValidationError

from userapp.models import UserProfile


class UserForm(forms.ModelForm):
    # 1. 新增一个字段（password2）
    password2 = forms.CharField(max_length=50,
                                label='确认口令')

    class Meta:
        # 当前Form表单对应的模型类
        # 作用： 读取数据
        model = UserProfile

        # 显示或验证的字段
        # 如果验证所有字段，则'__all__'
        # 如果指定字段, 则 ［'字段名1', '字段名2', ...］
        fields = '__all__'

        # 当前Form如果生成字段标签时，显示的label的名称
        # 在网页中: {{ form.as_p }}
        labels = {
           'username': '用户名',
            'password': '口令'
        }

        # 验证错误消息
        error_messages = {
            'username': {'required': '用户名不能为空'},
            'password': {'required': '口令不能为空'},
            'phone': {'required': '手机号不能为空'},
            'photo': {'required': '头像不能为空'},
            'password2': {'required': '确认口令不能为空'},
        }



    # 验证数据（是否空）
    # 验证两次密码是否相同
    # （问题： 如何从请求中获取model中不存在的属性字段值）
    def is_valid(self):
        # cleaned_data 是dict类型，只有执行form.is_valid()函数,才会生成的"干净"的数据
        return super().is_valid()

    # 清除password2数据的空格
    def clean_password2(self):
        passwd1 = self.cleaned_data.get('password')
        passwd2 = self.cleaned_data.get('password2')
        if passwd1 != passwd2:
            # 如果抛出异常时，则会由form的errors收集
            raise ValidationError('两次密码不相同')

        return passwd1

    # 通过正则验证手机号
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')

        return phone