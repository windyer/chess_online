#coding=utf-8
import re
from rest_framework import serializers
alnum_reg = re.compile(r'^[a-zA-Z0-9]+$')
simple_reg = re.compile(r'^(([a-zA-Z0-9]))\1+$')
simple_group = ['123456', '1234567', '12345678', '123456789']

class Register(serializers.Serializer):
    pass

class ChangePassword(serializers.Serializer):
    password = serializers.CharField(min_length=6)
    new_password = serializers.CharField(min_length=6)

class BindAccount(serializers.Serializer):
    user_name = serializers.CharField(max_length=100)
    password = serializers.CharField(max_length=50)

class ForgetPasswordRequest(serializers.Serializer):
    user_name = serializers.CharField(max_length=100)


class ResetPasswordRequest(serializers.Serializer):

    new_password = serializers.CharField(min_length=6, max_length=16)
    confirm_password = serializers.CharField(min_length=6, max_length=16)

    def validate(self, attrs):
        new_password = attrs['new_password']
        confirm_password = attrs['confirm_password']

        if new_password != confirm_password:
            raise serializers.ValidationError(u"两次输入的密码不相同")
        if (simple_reg.match(new_password) or
                simple_reg.match(confirm_password) or
                new_password in simple_group or
                confirm_password in simple_group):
            raise serializers.ValidationError(u'密码设置过于简单')
        if not (alnum_reg.match(new_password) and alnum_reg.match(confirm_password)):
            raise serializers.ValidationError(u'输入错误')

        attrs['new_password'] = new_password
        attrs['confirm_password'] = confirm_password
        return attrs
