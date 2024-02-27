from django.shortcuts import render
from django.db import connection
from django.forms import model_to_dict
from django.db.models import Q
from django.core import serializers
from django.contrib.auth.decorators import login_required

from public.views_com import message_writing
from public.auth_token import auth_token
from nb.models import *
from public.common import *
from public.response import JsonResponse


@auth_token()
def modify_subject(request):
    """所有主题设置"""
    if request.method == POST:
        body = handle_json(request)
        if not body:
            return JsonResponse.JsonException()
        code = is_int(body.get("code"))
        value = is_int(body.get("value"))
        if not code or not value:
            return JsonResponse.ParameException()
        model = query_model(request, Customizer)
        try:
            model.filter(code=code).update(value=value)
        except Exception as error:
            return JsonResponse.DatabaseException(data=str(error))
        return JsonResponse.OK()


@auth_token()
def subject(request):
    """获取整体主题设置"""
    if request.method == POST:
        info = request_get_search(request)
        model = query_model(request, Customizer)
        layout = model_to_dict(model.get(code=LayoutCode))
        info.update({
            "obj": serializers.serialize("json", model, cls=LazyEncoder),
            "layout": layout,
        })
        return JsonResponse.OK(data=info)


@auth_token()
def theme(request):
    """获取页面整体主题设置"""
    if request.method == POST:
        info = request_get_search(request)
        model = query_model(request, Customizer).filter(code=LayoutCode)
        info.update({
            "obj": serializers.serialize("json", model, cls=LazyEncoder),
        })
        return JsonResponse.OK(data=info)


def upload_poetry(request):
    """导入诗词"""
    if request.method == POST:
        if not query_model(request, Author).exists():
            file_list = os.listdir(UploadPoetryPath)
            if not file_list:
                return JsonResponse.EmptyException()
            for file in file_list:
                file_path = os.path.join(UploadPoetryPath, file)
                data_list = read_file(file_path)
                for sql in data_list:
                    try:
                        with connection.cursor() as cur:
                            cur.execute(sql)
                    except Exception as error:
                        pass
        return JsonResponse.OK()


def poetry(request):
    """
    诗词推荐列表
    """
    if request.method == POST:
        # 随机返回一条数据 filter 等于  exclude 不等于
        poetry_type = PoetryTypeList[randint(0, len(PoetryTypeList) - 1)]
        poetry_list = query_model(request, Poetry).filter(type=poetry_type).exclude(
            Q(phrase="") | Q(explain="")).order_by('?')[:HomeNumber]
        obj_list = list()
        for data in poetry_list:
            result = {
                "id": str(data.id),
                "poetry_name": data.name,
                "type": data.type,
                "phrase": "".join(data.phrase.splitlines()),
                "explain": "".join(data.explain.splitlines()),
                "author": data.author.name if data.author else "",
                "dynasty": data.author.dynasty if data.author else "",
            }
            obj_list.append(result)
        return JsonResponse.OK(data=obj_list)


@login_required
def message_list(request):
    """消息提醒页面"""
    if request.method == GET:
        info = request_get_search(request)
        search = info["search"]
        if search:
            obj_list = query_model(request, Message).filter(is_look=False).order_by("-create_date")[0:auxiliaryNumber]
        else:
            obj_list = query_model(request, Message).order_by("-create_date")[0:auxiliaryNumber]
        info = pagination(paging_data(obj_list, info))
        return render(request, "home/message.html", info)


@auth_token()
def message_home(request):
    """首页消息提醒"""
    if request.method == POST:
        model = query_model(request, Message)
        message_list = model.filter(Q(date=date.today()) & Q(is_look=False)).order_by("-create_date")
        flag = True
        if not message_list:
            flag = False
            message_list = model.filter(Q(date=date.today()) & Q(is_look=True)).order_by("-create_date")
        result = {
            "number": len(message_list),
            "flag": flag,
            "data": [],
        }
        if not message_list:
            return JsonResponse.OK(data=result)
        for message in message_list[:HomeNumber]:
            result["data"].append({
                "time": format_time(message.create_date),
                "obj_id": message.obj_id,
                "name": message.name,
                "type": message.type,
            })
        return JsonResponse.OK(data=result)


@auth_token()
def message_look(request):
    """全部通知标记为已读"""
    if request.method == POST:
        model = query_model(request, Message).filter(is_look=False)
        if model.exists():
            model.update(is_look=True)
        else:
            return JsonResponse.EmptyException()
        info = request_get_search(request)
        message = query_model(request, Message).first()
        setattr(message, "name", "未读通知标记为已读")
        operation_record(request, model=message, action_flag=9)
        return JsonResponse.OK(data=info)


@login_required
def partners_list(request):
    """基础信息-业务伙伴 页面"""
    if request.method == GET:
        info = request_get_search(request)
        model = query_model(request, Partners)
        search = info["search"]
        if search:
            obj_list = model.filter(name__contains=search).order_by("-create_date")
        else:
            obj_list = model.order_by("-create_date")
        info = pagination(paging_data(obj_list, info))
        return render(request, "home/partners.html", info)


@auth_token()
def partners_save(request):
    """保存业务伙伴数据"""
    if request.method == POST:
        body = handle_json(request)
        if not body:
            return JsonResponse.JsonException()
        partners_id = body.get("partners_id")
        name = body.get("name")
        partners_type = body.get("type")
        telephone = body.get("telephone")
        address = body.get("address")
        remark = body.get("remark")
        model = query_model(request, Partners).order_by("-create_date")
        model_obj = model.filter(name=name)
        if partners_id:
            if model_obj.exclude(id=partners_id).exists():
                return JsonResponse.RepeatException(message="业务伙伴名称已存在")
        else:
            if model_obj.exists():
                return JsonResponse.RepeatException(message="业务伙伴名称已存在")
        try:
            user_id = request.session.get("user_id")
            if partners_id:
                partners = model_obj.get(id=partners_id)
            else:
                partners = Partners()
            partners.code = is_int(model[0].code) + 1 if model.exists() else InitNumber
            partners.pinyin_code = name_to_pinyin(name)
            partners.name = name
            partners.type = partners_type
            partners.telephone = telephone
            partners.address = address
            partners.remark = remark
            partners.user_id = user_id
            partners.save()
        except Exception as error:
            return JsonResponse.DatabaseException(data=str(error))
        repr_text = "业务伙伴"
        message_writing(MessagePartners.format(name=name), partners.id, date.today(), "")
        operation_record(request, model=partners, model_id=partners_id, repr_text=repr_text)
        return JsonResponse.OK()


@auth_token()
def partners_info(request, partners_id):
    """返回指定业务伙伴数据"""
    if request.method == POST:
        info = request_get_search(request)
        model = query_model(request, Partners).filter(id=partners_id)
        info.update({
            "obj": serializers.serialize("json", model, cls=LazyEncoder),
        })
        return JsonResponse.OK(data=info)


@auth_token()
def partners_status(request, partners_id):
    """修改业务伙伴状态"""
    if request.method == POST:
        body = handle_json(request)
        if not body:
            return JsonResponse.JsonException()
        user_id = request.session.get("user_id")
        status = 1 if is_int(body.get("status")) == 0 else 0
        model = query_model(request, Partners).filter(id=partners_id)
        if not model.exists():
            return JsonResponse.EmptyException()
        partners = model.get(id=partners_id)
        try:
            partners.user_id = user_id
            partners.status = status
            partners.save()
        except Exception as error:
            return JsonResponse.DatabaseException(data=str(error))
        info = request_get_search(request)
        info = delete_jump(info, model)
        repr_text = "业务伙伴"
        operation_record(request, model=partners, action_flag=9, repr_text=repr_text)
        return JsonResponse.OK(data=info)


@auth_token()
def partners_del(request, partners_id):
    """删除业务伙伴数据"""
    if request.method == POST:
        user_id = request.session.get("user_id")
        model = query_model(request, Partners).filter(id=partners_id)
        if not model.exists():
            return JsonResponse.EmptyException()
        partners = model.get(id=partners_id)
        try:
            partners.user_id = user_id
            partners.save()
            partners.delete()
        except Exception as error:
            return JsonResponse.DatabaseException(data=str(error))
        info = request_get_search(request)
        info = delete_jump(info, model)
        repr_text = "业务伙伴"
        operation_record(request, model=partners, action_flag=3, repr_text=repr_text)
        return JsonResponse.OK(data=info)


@login_required
def operate_log_list(request):
    """操作日志页面"""
    if request.method == GET:
        info = request_get_search(request)
        search = info["search"]
        if search and search != "0":
            obj_list = LogEntry.objects.filter(action_flag=search).order_by("-action_time")[0:auxiliaryNumber]
        else:
            obj_list = LogEntry.objects.all().order_by("-action_time")[0:auxiliaryNumber]
        info = pagination(paging_data(obj_list, info))
        return render(request, "home/operateLog.html", info)


@auth_token()
def operate_action(request):
    """获取所有操作动作"""
    if request.method == POST:
        return JsonResponse.OK(data=ActionMaKe)
