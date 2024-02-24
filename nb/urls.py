#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time  :  13:03
# @Author: 李先生大发
# @File  : urls.py
# @doc   :
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from nb import views

app_name = "nb"
urlpatterns = [
                  path("modify/subject/", views.modify_subject, name="modify_subject"),  # 主题设置
                  path("subject/", views.subject, name="subject"),  # 主题设置
                  path("theme/", views.theme, name="theme"),  # 页面整体主题设置
                  path("upload/poetry/", views.upload_poetry, name="upload_poetry"),  # 导入诗词
                  path("poetry/", views.poetry, name="poetry"),  # 展示诗词
                  path("message/warn/", views.message_warn, name="message_warn"),  # 消息提醒
                  path("message/home/", views.message_home, name="message_home"),  # 消息提醒
                  path("partners/", views.partners_list, name="partners"),  # 业务伙伴
                  path("partners/save/", views.partners_save, name="partners_save"),  # 业务伙伴
                  path("partners/info/<uuid:partners_id>/", views.partners_info, name="partners_info"),  # 业务伙伴
                  path("partners/status/<uuid:partners_id>/", views.partners_status, name="partners_status"),  # 业务伙伴
                  path("partners/del/<uuid:partners_id>/", views.partners_del, name="partners_del"),  # 业务伙伴
                  path("operate/log/", views.operate_log_list, name="operate_log"),  # 操作记录
                  path("operate/action/", views.operate_action, name="operate_action"),  # 操作记录

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
