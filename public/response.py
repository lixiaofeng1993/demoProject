#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# 创 建 人: 李先生
# 文 件 名: response.py
# 创建时间: 2022/11/19 0019 23:47
# @Version：V 0.1
# @desc :
import json
from django.http import HttpResponse


class JsonResponse(HttpResponse):
    def __init__(self, code=200, message="ok", data=None):
        response = dict()
        response["code"] = code
        response["message"] = message
        response["data"] = data
        self.headers = {}
        super(JsonResponse, self).__init__(json.dumps(response, ensure_ascii=False), content_type="application/json", )

    @staticmethod
    def OK(message="ok", data=None):
        response = JsonResponse(200, message, data)
        return response

    @staticmethod
    def BadRequest(message="请求出现异常", data=None):
        response = JsonResponse(400, message, data)
        return response

    @staticmethod
    def ServerError(message="系统异常", data=None):
        return JsonResponse(500, message, data)

    @staticmethod
    def Unauthorized(message="账号登录过期", data=None):
        return JsonResponse(100000, message, data)

    @staticmethod
    def MethodNotAllowed(message="请求方式错误", data=None):
        return JsonResponse(100001, message, data)

    @staticmethod
    def LoginRepeatException(message="帐号已登录", data=None):
        return JsonResponse(100002, message, data)

    @staticmethod
    def CheckException(message="检查字段存在异常", data=None):
        return JsonResponse(100003, message, data)

    @staticmethod
    def JsonException(message="传参类型错误", data=None):
        return JsonResponse(100004, message, data)

    @staticmethod
    def DatabaseException(message="操作数据库出现错误", data=None):
        return JsonResponse(100005, message, data)

    @staticmethod
    def RepeatException(message="数据重复异常", data=None):
        return JsonResponse(100006, message, data)

    @staticmethod
    def TokenException(message="token参数错误", data=None):
        return JsonResponse(100007, message, data)

    @staticmethod
    def TimeException(message="时间格式错误", data=None):
        return JsonResponse(100008, message, data)

    @staticmethod
    def EmptyException(message="查询数据为空", data=None):
        return JsonResponse(100009, message, data)

    @staticmethod
    def CodeException(message="验证码错误", data=None):
        return JsonResponse(100010, message, data)

    @staticmethod
    def UserException(message="帐号不存在", data=None):
        return JsonResponse(100011, message, data)

    @staticmethod
    def ParameException(message="传参异常", data=None):
        return JsonResponse(100012, message, data)

    @staticmethod
    def EqualException(message="数据不一致", data=None):
        return JsonResponse(100013, message, data)
