#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time  :  13:03
# @Author: 李先生大发
# @File  : views.py
# @doc   :
import re
from django.shortcuts import render
from django.core.cache import cache
from django.http import HttpResponseRedirect
from django.db.models import Q
from django.contrib import auth  # django认证系统
from django.contrib.auth.models import User
from django.core import serializers
from django.contrib.auth.decorators import login_required

from public.jwt_sign import create_access_token
from public.auth_token import auth_token
from public.response import JsonResponse
from nb.models import Security
from public.common import *
from public.log import logger


@login_required
def index(request):
    info = request_get_search(request)
    return render(request, "home/index.html", info)


def login(request):
    if request.method == GET:
        info = request_get_search(request)
        return render(request, "login/login.html", info)
    elif request.method == POST:
        body = handle_json(request)
        if not body:
            return JsonResponse.JsonException()
        username = body.get('username', '')
        password = body.get('password', '')
        user = auth.authenticate(username=username, password=password)
        if user is None:
            return JsonResponse.CheckException(message="用户名或者密码错误")
        auth.login(request, user)
        user = User.objects.get(username=username)
        token = cache.get(username)
        if token:  # 避免重复登录
            cache.delete(username)
        request.session["user"] = username
        request.session["user_id"] = user.id
        request.session["is_staff"] = user.is_staff
        request.session["is_super"] = user.is_superuser  # 是否是超级管理员
        result = {
            "id": user.id,
            "username": username,
            "token": token,
        }
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        token = create_access_token({"sub": username}, expires_delta=access_token_expires)
        cache.set(username, token, ACCESS_TOKEN_EXPIRE_MINUTES * 60)
        result["token"] = token
        setattr(user, "name", "登陆系统")
        operation_record(request, model=user, action_flag=5)
        return JsonResponse.OK(data=result)


@login_required
@auth_token()
def modify_password(request):
    """修改密码"""
    if request.method == GET:
        info = request_get_search(request)
        obj = query_model(request, Security).filter(user_id=info["user_id"]).order_by("-update_date").first()
        info["obj"] = obj
        return render(request, "login/modifyPwd.html", info)
    elif request.method == POST:
        body = handle_json(request)
        if not body:
            return JsonResponse.JsonException()
        username = request.session.get("user")
        password = body.get("password")
        new_password = body.get("newPassword")
        confirm_password = body.get("confirmPassword")
        problem = body.get("problem")
        answer = body.get("answer")
        user = User.objects.get(username=username)
        if not problem and not answer:
            return JsonResponse.CheckException(message="请输入密保问题和答案")
        if password and new_password and confirm_password:
            verify = auth.authenticate(username=username, password=password)
            if verify is None:
                return JsonResponse.CheckException(message="原密码错误")
            if password == new_password:
                return JsonResponse.RepeatException(message="新密码和原密码相同")
            if new_password != confirm_password:
                return JsonResponse.EqualException(message="新密码和确认密码不一致")
            try:
                user.set_password(new_password)
                user.save()
            except Exception as error:
                return JsonResponse.DatabaseException(data=str(error))
        model = query_model(request, Security).filter(user_id=user.id)
        flag = False
        try:
            if model.exists():
                if model.filter(problem=problem).exists():
                    flag = True
                    security = model.get(problem=problem)
                    security.answer = answer
                    security.save()
                else:
                    model.update(is_delete=1)
            if not flag:
                security = Security()
                security.problem = problem
                security.answer = answer
                security.user_id = user.id
                security.save()
        except Exception as error:
            print(error)
            return JsonResponse.DatabaseException(data=str(error))
        setattr(user, "name", "修改密码")
        operation_record(request, model=user, action_flag=8)
        return JsonResponse.OK()


def rest_password(request):
    """重置密码"""
    if request.method == GET:
        info = request_get_search(request)
        return render(request, "login/resetPwd.html", info)
    elif request.method == POST:
        body = handle_json(request)
        if not body:
            return JsonResponse.JsonException()
        username = body.get("username")
        new_password = body.get("newPassword")
        confirm_password = body.get("confirmPassword")
        if new_password != confirm_password:
            return JsonResponse.EqualException(message="新密码和确认密码不一致")
        try:
            user = User.objects.get(username=username)
            user.set_password(new_password)
            user.save()
        except User.DoesNotExist:
            return JsonResponse.UserException()
        except Exception as error:
            return JsonResponse.DatabaseException(data=str(error))
        setattr(user, "name", "重置密码")
        operation_record(request, model=user, action_flag=8)
        return JsonResponse.OK()


def forget_password(request):
    """忘记密码"""
    if request.method == GET:
        info = request_get_search(request)
        return render(request, "login/security.html", info)
    elif request.method == POST:
        body = handle_json(request)
        if not body:
            return JsonResponse.JsonException()
        username = body.get("username")
        try:
            user = User.objects.get(username=username)
            model = query_model(request, Security).filter(user_id=user.id)
            if not model.exists():
                return JsonResponse.EmptyException(message="未设置密保问题")
            info = {
                "problem": model.first().problem,
                "answer": model.first().answer,
            }
        except Exception as error:
            return JsonResponse.UserException()
        setattr(user, "name", "验证密保问题")
        operation_record(request, model=user, action_flag=8)
        return JsonResponse.OK(data=info)


@login_required
def logout(request):
    if request.method == GET:
        info = request_get_search(request)
        user = User.objects.get(username=info["user"])
        setattr(user, "name", "退出系统")
        operation_record(request, model=user, action_flag=6)
        cache.delete(info["user"])
        auth.logout(request)  # 退出登录
        return render(request, "login/logout.html", info)


@login_required
@auth_token()
def lock(request):
    if request.method == GET:
        info = request_get_search(request)
        user = User.objects.get(username=info["user"])
        setattr(user, "name", "锁定系统")
        operation_record(request, model=user, action_flag=6)
        return render(request, "login/lockScreen.html", info)
    elif request.method == POST:
        body = handle_json(request)
        if not body:
            return JsonResponse.JsonException()
        username = request.session.get("user")
        password = body.get('password', '')
        user = auth.authenticate(username=username, password=password)
        if user is None:
            return JsonResponse.CheckException(message="密码错误")
        setattr(user, "name", "解锁系统")
        operation_record(request, model=user, action_flag=5)
        return JsonResponse.OK()


def page_not_found(request, exception, template_name='home/404.html'):
    logger.error(f"页面出现异常 ===>>> {exception}")
    return render(request, template_name)


def server_error(exception, template_name='home/500.html'):
    logger.error(f"系统出现异常 ===>>> {exception}")
    return render(exception, template_name)
