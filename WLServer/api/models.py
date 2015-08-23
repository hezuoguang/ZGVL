# coding:utf-8
from django.db import models

# Create your models here.

# 用户模型
class User(models.Model):
    # 账号,唯一标识
    uid = models.CharField(max_length = 16, primary_key = True, verbose_name = "用户名")
    # 密码
    pwd = models.CharField(max_length = 255, verbose_name = "密码")
    # 昵称
    name = models.CharField(max_length = 16, default = "微米", verbose_name = "昵称")
    # 头像
    photo = models.CharField(max_length = 1024, default = "http://7xl0k3.com1.z0.glb.clouddn.com/default.jpg", verbose_name = "头像")
    # 年龄
    age = models.PositiveSmallIntegerField(default = 0, verbose_name = "年龄")
    # 性别
    sex = models.CharField(max_length = 4, default = "未知", verbose_name = "性别")
    # 生日
    birthday = models.DateTimeField(verbose_name = "生日", auto_now_add = True)
    # 城市
    city = models.CharField(max_length = 255, default = "怀化", verbose_name = "城市")
    # 好友们
    friends = models.ManyToManyField("self", blank = True, verbose_name = "好友们")
    # 消息
    messgaes = models.ManyToManyField("Message", blank = True)
    # 添加好友消息
    newfriends = models.ManyToManyField("Newfriend", blank = True)
    # 授权标识
    access_token = models.TextField(verbose_name = "授权标识")
    def __unicode__(self):
        return self.uid + "(" + self.name + ")"


# 消息模型
class Message(models.Model):
    # 消息内容,文字消息为:消息内容; gif表情消息为:gif表情对应的图片名					称 名称;语音,图片消息为:资源的url
    text = models.CharField(max_length = 1024, verbose_name = "消息内容")
    # 消息创建时间
    create_time = models.DateTimeField(auto_now_add = True, verbose_name = "创建时间")
    # 消息类型 (0, "文本消息"),(1, "gif表情消息"),(2, "图片消息"),(3, "语音消息")
    type = models.PositiveSmallIntegerField(verbose_name = "消息类型", default = 0)
    # 接收者 user模型
    to_user = models.ForeignKey(User, verbose_name = "接收者")
    def __unicode__(self):
        return self.text

# 添加好友消息模型
class Newfriend(models.Model):
    # 接收者 user模型
    to_user = models.ForeignKey(User, verbose_name = "接收者")
    # 请求说明
    text = models.CharField(max_length = 1024, verbose_name = "请求说明")
    # 处理状态,同意\拒绝\忽略\处理中((0, "处理中"),(1, "拒绝"),(3, "同意"))
    status = models.PositiveSmallIntegerField(verbose_name = "处理状态", default = 0)
    # 消息创建时间
    create_time = models.DateTimeField(auto_now_add = True, verbose_name = "创建时间")
    def __unicode__(self):
        return "(" + self.text + ")"

# 状态模型,类似微博,朋友圈
class Status(models.Model):
    # 状态内容
    text = models.CharField(max_length = 1024, verbose_name = "状态内容")
    # 创建时间
    create_time = models.DateTimeField(auto_now_add = True, verbose_name = "创建时间")
    # 图片链接 数组
    pics = models.TextField(verbose_name = "图片地址", blank = True)
    #发送者 user模型
    from_user = models.ForeignKey(User, verbose_name = "发送者")
    def __unicode__(self):
        return (str)(self.id) + "(" + self.text + ")"


# 状态的评论模型
class Comment(models.Model):
    # 评论内容
    text = models.CharField(max_length = 255, verbose_name = "评论内容")
    # 创建时间
    create_time = models.DateTimeField(auto_now_add = True, verbose_name = "创建时间")
    # 发送者 user模型
    from_user = models.ForeignKey(User, verbose_name = "发送者")
    # 所评论的状态
    status = models.ForeignKey(Status, verbose_name = "所评论的状态")
    def __unicode__(self):
        return "(" + self.text + ")"



