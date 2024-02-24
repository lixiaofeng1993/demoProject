#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time  :  20:15
# @Author: 李先生大发
# @File  : views_com.py
# @doc   :

from nb.models import Message
from datetime import date


def message_writing(name: str, obj_id: str, date_time: date, link_type: str):
    """
    写入消息提醒数据
    """
    try:
        message = Message()
        message.name = name
        message.obj_id = obj_id
        message.date = date_time
        message.type = link_type
        message.save()
    except Exception as error:
        raise Exception(str(error))
