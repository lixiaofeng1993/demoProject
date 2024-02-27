#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# 创 建 人: 李先生
# 文 件 名: conf.py
# 创建时间: 2022/11/20 0020 12:47
# @Version：V 0.1
# @desc :
import os, io
from django.conf import settings


def check_dir(path: str) -> str:
    """
    检查目录是否存在，不存在则创建目录
    :param path:
    :return: path
    """
    if not os.path.exists(path):
        os.makedirs(path)
    return path


def check_file(path):
    """
    检查文件是否存在，不存在则创建
    :param path:
    :return:
    """

    if not os.path.exists(path):
        with io.open(path, "w", encoding="utf-8") as f:
            pass
        return path
    else:
        return path


def read_file(path: str):
    """
    读取文件
    :param path:
    :return:
    """
    if os.path.isfile(path):
        with io.open(path, "r", encoding="utf-8") as f:
            data = f.readlines()
            return data


# token
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 720
# 请求方式
GET = "GET"
POST = "POST"

# 导入文件路径
UploadPath = check_dir(os.path.join(settings.BASE_DIR, "upload"))
# 导出文件路径
ExportPath = check_dir(os.path.join(settings.BASE_DIR, "media", "download"))
# 导入诗词数据路径
UploadPoetryPath = check_dir(os.path.join(settings.BASE_DIR, "tools", "sql"))

# 网站名称
SiteName = "Niubility"
# 默认密码
DefaultPassword = "123456"
# 分页
NumberOfPages = 10
# 首页展示数量
HomeNumber = 5
# 辅助数据展示数量
auxiliaryNumber = 100
# 验证码长度
CodeNumber = 6
# 邮箱密码
EmailPassword = "PLSECRVQWUXAADGN"
# 页面整体布局指定序号
LayoutCode = 5
# 数据初始编号
InitNumber = 10001

# 操作动作
ActionMaKe = {
    1: "新增",
    2: "编辑",
    3: "删除",
    5: "登陆",
    6: "注销",
    8: "密码",
    9: "状态",
}

# 诗词类型
PoetryTypeList = ['节日', '竹子', '梅花', '说苑', '淮南子', '边塞', '管子', '国语', '爱情', '红楼梦', '韩非子', '元宵节', '友情', '围炉夜话', '中庸', '写鸟',
                  '清明节', '写风', '冬天', '小窗幽记', '感恩', '山水', '秋天', '文心雕龙', '战国策', '贞观政要', '荀子', '醒世恒言', '黄河', '三国演义', '老师',
                  '左传', '母亲', '孟子', '增广贤文', '泰山', '格言联璧', '菜根谭', '荷花', '柳树', '田园', '端午节', '中秋节', '西湖', '长江', '尚书', '哲理',
                  '老子', '警世通言', '吕氏春秋', '伤感', '幼学琼林', '写云', '菊花', '月亮', '论衡', '晋书', '弟子规', '后汉书', '写雨', '写雪', '重阳节',
                  '桃花', '春天', '春节', '庐山', '思乡', '爱国', '商君书', '列子', '星星', '史记', '七夕节', '论语', '读书', '离别', '思念', '礼记',
                  '励志', '寒食节', '墨子', '水浒传', '夏天']

# 消息提醒页面展示文案
MessagePartners = "业务伙伴 {name} 数据更新"
