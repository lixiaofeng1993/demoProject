#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time  :  13:05
# @Author: 李先生大发
# @File  : common.py
# @doc   :

import json
import time
from django.contrib.admin.models import LogEntry
from django.contrib.admin.options import get_content_type_for_model
from typing import Dict, List, Union, Any, Optional
from django.core.serializers.json import DjangoJSONEncoder
from random import choice, randint
from decimal import Decimal  # 精确四舍五入保留两位小数
from xpinyin import Pinyin
from datetime import date, datetime, timedelta

from public.conf import *


def random_str(length: int = CodeNumber) -> str:
    """
    随机字符串
    """
    H = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
    salt = ""
    for i in range(length):
        salt += choice(H)
    return salt


def format_time(date_time: datetime) -> str:
    """
    格式化时间天，小时，分钟，秒
    """
    now = datetime.now()
    total_seconds = round((now - date_time).total_seconds())
    total_seconds = total_seconds if total_seconds > 0 else 1
    if total_seconds < 60:
        _time = f"{total_seconds}秒前"
    elif 60 <= total_seconds < 3600:
        _time = f"{round(total_seconds / 60)}分钟前"
    elif 3600 <= total_seconds < 86400:
        _time = f"{round(total_seconds / 3600)}小时前"
    elif 86400 <= total_seconds < 172800:
        _time = f"{round(total_seconds / 86400)}天前"
    else:
        _time = date_time.strftime("%Y-%m-%d %H:%M:%S")
    return _time


def surplus_second() -> int:
    """
    当天剩余秒数
    """
    today = date.today()
    today_end = f"{str(today)} 23:59:59"
    end_second = int(time.mktime(time.strptime(today_end, "%Y-%m-%d %H:%M:%S")))
    now_second = int(time.time())
    return end_second - now_second


def surplus_mouth() -> int:
    """
    当月剩余秒数
    """
    now = datetime.now()
    end_time = now + timedelta(days=30)
    total_seconds = (end_time - now).total_seconds()
    return int(total_seconds)


def operation_record(request, model, model_id="", action_flag=0, repr_text=""):
    """
    操作记录
    """
    if model_id and action_flag == 0:
        action_flag = 2
    elif action_flag == 0:
        action_flag = 1
    repr_text = ActionMaKe.get(action_flag) if not repr_text else repr_text
    change_message = f"{model.name}" if hasattr(model, "name") else ""
    user_id = request.session["user_id"] if request.session.get("user_id") else model.id
    if model_id:
        object_id = model_id
    elif model.id:
        object_id = model.id
    else:
        object_id = ""
    LogEntry.objects.log_action(
        user_id=user_id,
        content_type_id=get_content_type_for_model(model).id,
        object_id=object_id,
        object_repr=repr_text,
        action_flag=action_flag,
        change_message=change_message,
    )


def handle_json(request) -> Optional[Any]:
    """
    转化js json传参为dict
    """
    try:
        body = request.body.decode()
        body_dict = json.loads(body)
        return body_dict
    except json.JSONDecodeError as error:
        return


class LazyEncoder(DjangoJSONEncoder):
    """
    格式化modal时间转json
    """

    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        return super().default(obj)


def query_model(request, model: Any) -> Any:
    """
    用户权限
    超级管理员可以看所有，普通用户只能看自己的数据
    """
    # is_super = request.session.get("is_super")
    # if is_super:
    #     return model.objects.filter(is_delete=False)
    # else:
    #     user_id = request.session.get("user_id")
    #     return model.objects.filter(Q(user_id=user_id) & Q(is_delete=False))
    return model.objects.filter(is_delete=False)


def request_get_search(request) -> Dict:
    """
    封装获取get请求公共参数
    :param request:
    :return:
    """
    search = request.GET.get('search', '')
    query = request.GET.get('query', '')
    page = request.GET.get('page', '1')
    size = request.GET.get('size', '10')
    start_time = request.GET["start_time"] if request.GET.get('start_time') else ""
    end_time = request.GET["end_time"] if request.GET.get('end_time') else ""
    user = request.session.get("user")
    user_id = request.session.get("user_id")
    is_super = request.session.get("is_super")
    is_staff = request.session.get("is_staff")
    page = int(page) if page.isdigit() else 1
    size = int(size) if size.isdigit() else 10
    start = (page - 1) * size  # 起
    end = page * size  # 始
    # 列表序号
    page_flag = (page - 1) * size
    info = {
        "search": search,
        "query": query,
        "page": page,
        "size": size,
        "start_time": start_time,
        "end_time": end_time,
        "user": user,
        "user_id": user_id,
        "is_super": is_super,
        "is_staff": is_staff,
        "start": start,
        "end": end,
        "page_flag": page_flag,
        "siteName": SiteName,
        "actionMaKe": ActionMaKe.get(is_int(search)),
    }
    return info


def handle_price(price: Union[int, float]) -> Union[str, float]:
    """
    数据加单位
    """
    if price >= 100000000 or price <= -100000000:
        price = str(round(price / 100000000, 2)) + "亿"
    elif price >= 10000 or price <= -10000:
        price = str(round(price / 10000, 2)) + "万"
    else:
        price = round(price, 2)
    return price


def handle_rate(rate: Union[int, float]) -> str:
    """
    数据加 %
    """
    return str(round(rate, 2)) + "%"


def delete_jump(info, obj_list, detail=False):
    """
    删除跳转
    """
    page = info["page"]
    size = info["size"]
    number = len(obj_list) % size
    if number == 0 and len(obj_list) >= size and page != 1:
        info["page"] = page - 1
    return info


def is_int(s: str):
    """
    判断是否能转整数，报错返回0
    """
    if str(s).isdigit():
        return int(str(s))
    else:
        return 0


def is_number(s):
    """
    判断是否能转浮点数，报错返回0
    """
    try:
        s = float(s) if s else 0
        return float(s)
    except ValueError:
        return 0


def accurate_two_bit(number: int or str) -> float:
    """
    精确四舍五入保理两位小数
    """
    number = is_number(number)
    number = Decimal(f"{number}").quantize(Decimal("0.00"))
    return float(number)


def accurate_zero_bit(number: int or str) -> float:
    """
    精确四舍五入不保留小数位
    """
    number = is_number(number)
    number = Decimal(f"{number}").quantize(Decimal("0"))
    return int(number)


def name_to_pinyin(name: str):
    """
    汉字转拼音
    """
    pinyin = Pinyin()
    res = pinyin.get_pinyin(name)
    code = "".join(res.split("-")) if res else None
    return code


def file_iterator(file_path, chunk_size=512):
    """
    下载文件
    """
    with open(file_path, "rb") as f:
        while True:
            c = f.read(chunk_size)
            if c:
                yield c
            else:
                break


def paging_data(model, info):
    """
    处理分页数据
    """
    total_number = model.count()  # 总条数
    total_pages = total_number // info["size"]  # 总页数
    if total_number % info["size"] > 0:
        total_pages = total_pages + 1
    info["object_list"] = model[info["start"]:info["end"]]
    is_paginated = True if total_number > info["size"] else False  # 是否需要分页
    if info["page"] < 1:
        info["page"] = 1
    elif info["page"] > total_pages > 0:
        info["page"] = total_pages
    info["total_pages"] = total_pages
    info["total_number"] = total_number
    info["is_paginated"] = is_paginated
    return info


def pagination(info) -> Dict:
    """
    牛掰的分页
    """
    # 获得分页后的总页数
    # 获得用户当前请求的页码号
    total_pages, page_number, is_paginated = info["total_pages"], info["page"], info["is_paginated"]
    if not is_paginated:
        # 如果没有分页，则无需显示分页导航条，不用任何分页导航条的数据，因此返回一个空的字典
        return info

    # 当前页左边连续的页码号，初始值为空
    left = []

    # 当前页右边连续的页码号，初始值为空
    right = []

    # 标示第 1 页页码后是否需要显示省略号
    left_has_more = False

    # 标示最后一页页码前是否需要显示省略号
    right_has_more = False

    # 标示是否需要显示第 1 页的页码号。
    # 因为如果当前页左边的连续页码号中已经含有第 1 页的页码号，此时就无需再显示第 1 页的页码号，
    # 其它情况下第一页的页码是始终需要显示的。
    # 初始值为 False
    first = False

    # 标示是否需要显示最后一页的页码号。
    # 需要此指示变量的理由和上面相同。
    last = False

    # 获得整个分页页码列表，比如分了四页，那么就是 [1, 2, 3, 4]
    page_range = range(1, total_pages + 1)

    if page_number == 1:
        # 如果用户请求的是第一页的数据，那么当前页左边的不需要数据，因此 left=[]（已默认为空）。
        # 此时只要获取当前页右边的连续页码号，
        # 比如分页页码列表是 [1, 2, 3, 4]，那么获取的就是 right = [2, 3]。
        # 注意这里只获取了当前页码后连续两个页码，你可以更改这个数字以获取更多页码。
        right = page_range[page_number:page_number + 2]

        # 如果最右边的页码号比最后一页的页码号减去 1 还要小，
        # 说明最右边的页码号和最后一页的页码号之间还有其它页码，因此需要显示省略号，通过 right_has_more 来指示。
        if right[-1] < total_pages - 1:
            right_has_more = True

        # 如果最右边的页码号比最后一页的页码号小，说明当前页右边的连续页码号中不包含最后一页的页码
        # 所以需要显示最后一页的页码号，通过 last 来指示
        if right[-1] < total_pages:
            last = True

    elif page_number == total_pages:
        # 如果用户请求的是最后一页的数据，那么当前页右边就不需要数据，因此 right=[]（已默认为空），
        # 此时只要获取当前页左边的连续页码号。
        # 比如分页页码列表是 [1, 2, 3, 4]，那么获取的就是 left = [2, 3]
        # 这里只获取了当前页码后连续两个页码，你可以更改这个数字以获取更多页码。
        left = page_range[(page_number - 3) if (page_number - 3) > 0 else 0:page_number - 1]

        # 如果最左边的页码号比第 2 页页码号还大，
        # 说明最左边的页码号和第 1 页的页码号之间还有其它页码，因此需要显示省略号，通过 left_has_more 来指示。
        if left[0] > 2:
            left_has_more = True

        # 如果最左边的页码号比第 1 页的页码号大，说明当前页左边的连续页码号中不包含第一页的页码，
        # 所以需要显示第一页的页码号，通过 first 来指示
        if left[0] > 1:
            first = True
    else:
        # 用户请求的既不是最后一页，也不是第 1 页，则需要获取当前页左右两边的连续页码号，
        # 这里只获取了当前页码前后连续两个页码，你可以更改这个数字以获取更多页码。
        left = page_range[(page_number - 3) if (page_number - 3) > 0 else 0:page_number - 1]
        right = page_range[page_number:page_number + 2]

        # 是否需要显示最后一页和最后一页前的省略号
        if right[-1] < total_pages - 1:
            right_has_more = True
        if right[-1] < total_pages:
            last = True

        # 是否需要显示第 1 页和第 1 页后的省略号
        if left[0] > 2:
            left_has_more = True
        if left[0] > 1:
            first = True
    info.update({
        "left": left,
        "right": right,
        "left_has_more": left_has_more,
        "right_has_more": right_has_more,
        "first": first,
        "last": last,
    })
    return info
