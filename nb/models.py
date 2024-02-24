import uuid
from django.db import models
import django.utils.timezone as timezone
from django.contrib.auth.models import User
from bulk_update_or_create import BulkUpdateOrCreateQuerySet


class Customizer(models.Model):
    """
    主题自定义
    """
    id = models.UUIDField(primary_key=True, max_length=32, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, null=False, help_text="主题名称")
    code = models.IntegerField(default=0, null=True, help_text="主题编码")
    zh_name = models.CharField(max_length=100, null=False, help_text="主题中文名称")
    value = models.IntegerField(default=0, null=True, help_text="主题值")

    is_delete = models.BooleanField(default=False, help_text="是否删除")
    update_date = models.DateTimeField("更新时间", auto_now=True, help_text="更新时间")
    remark = models.TextField(default=None, null=True, help_text="备注")

    user = models.ForeignKey(User, on_delete=models.CASCADE, default="", null=True, help_text="用户ID")

    class Meta:
        db_table = "customizer"

    def delete(self, using=None, keep_parents=False):
        self.is_delete = True
        self.save()


class Author(models.Model):
    """
    诗人信息
    """
    objects = BulkUpdateOrCreateQuerySet.as_manager()

    id = models.UUIDField(primary_key=True, max_length=32, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=20, null=False, help_text="诗人名称")
    dynasty = models.CharField(max_length=20, default=None, help_text="诗人所属朝代")
    introduce = models.TextField(default=None, help_text="诗人简介")

    is_delete = models.BooleanField(default=False, help_text="是否删除")
    update_date = models.DateTimeField("更新时间", auto_now=True, help_text="更新时间")
    create_date = models.DateTimeField("保存时间", default=timezone.now)

    class Meta:
        db_table = "author"

    def delete(self, using=None, keep_parents=False):
        self.is_delete = True
        self.save()


class Poetry(models.Model):
    """
    诗词名句
    """
    objects = BulkUpdateOrCreateQuerySet.as_manager()

    id = models.UUIDField(primary_key=True, max_length=32, default=uuid.uuid4, editable=False)
    type = models.CharField(max_length=20, default=None, help_text="诗词类型")
    phrase = models.CharField(max_length=200, default=None, help_text="名句")
    explain = models.TextField(default=None, help_text="名句解释")
    appreciation = models.TextField(default=None, help_text="名句赏析")
    name = models.CharField(max_length=200, null=False, help_text="诗词名称")
    original = models.TextField(default=None, help_text="诗词原文")
    translation = models.TextField(default=None, help_text="诗词译文")
    background = models.TextField(default=None, help_text="创作背景")
    url = models.CharField(max_length=200, default=None, help_text="诗词地址")

    is_delete = models.BooleanField(default=False, help_text="是否删除")
    update_date = models.DateTimeField("更新时间", auto_now=True, help_text="更新时间")
    create_date = models.DateTimeField("保存时间", default=timezone.now)

    author = models.ForeignKey(Author, on_delete=models.CASCADE, default="", null=True, help_text="诗人ID")

    class Meta:
        db_table = "poetry"

    def delete(self, using=None, keep_parents=False):
        self.is_delete = True
        self.save()


class Security(models.Model):
    """密保问题"""
    objects = BulkUpdateOrCreateQuerySet.as_manager()

    id = models.UUIDField(primary_key=True, max_length=32, default=uuid.uuid4, editable=False)
    problem = models.CharField(max_length=200, default=None, help_text="问题")
    answer = models.CharField(max_length=100, default=None, help_text="答案")

    is_delete = models.BooleanField(default=False, help_text="是否删除")
    update_date = models.DateTimeField("更新时间", auto_now=True, help_text="更新时间")
    remark = models.TextField(default=None, null=True, help_text="备注")

    user = models.ForeignKey(User, on_delete=models.CASCADE, default="", null=True, help_text="用户ID")

    class Meta:
        db_table = "security"

    def delete(self, using=None, keep_parents=False):
        self.is_delete = True
        self.save()


class Partners(models.Model):
    """
    业务伙伴
    """
    objects = BulkUpdateOrCreateQuerySet.as_manager()

    id = models.UUIDField(primary_key=True, max_length=32, default=uuid.uuid4, editable=False)
    code = models.CharField(max_length=50, null=False, help_text="伙伴编码")
    pinyin_code = models.CharField(max_length=50, null=False, help_text="拼音编码")
    name = models.CharField(max_length=100, null=False, help_text="伙伴名称")
    address = models.CharField(max_length=200, null=False, help_text="伙伴地址")
    telephone = models.CharField(max_length=100, null=False, help_text="联系方式")
    status = models.IntegerField(default=0, null=True, help_text="伙伴状态")
    type = models.IntegerField(default=0, null=True, help_text="伙伴类型")

    is_delete = models.BooleanField(default=False, help_text="是否删除")
    update_date = models.DateTimeField("更新时间", auto_now=True, help_text="更新时间")
    create_date = models.DateTimeField("保存时间", default=timezone.now)
    remark = models.TextField(default=None, null=True, help_text="备注")

    user = models.ForeignKey(User, on_delete=models.CASCADE, default="", null=True, help_text="用户ID")

    class Meta:
        db_table = "partners"
        indexes = []

    def delete(self, using=None, keep_parents=False):
        self.is_delete = True
        self.save()


class Message(models.Model):
    """
    消息数据
    """
    id = models.UUIDField(primary_key=True, max_length=32, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=20, null=False, help_text="消息内容")
    obj_id = models.CharField(max_length=50, null=True, help_text="对象ID")
    type = models.CharField(max_length=20, null=True, help_text="跳转页面")
    date = models.DateTimeField("写入时间", null=True, help_text="写入时间(天)")
    is_look = models.BooleanField(default=False, help_text="是否已读")

    is_delete = models.BooleanField(default=False, help_text="是否删除")
    update_date = models.DateTimeField("更新时间", auto_now=True, help_text="更新时间")
    create_date = models.DateTimeField("保存时间", default=timezone.now)

    class Meta:
        db_table = "message"

    def delete(self, using=None, keep_parents=False):
        self.is_delete = True
        self.save()
