# -*- coding: UTF-8 -*- 
__author__ = 'weimi'
from api.models import *
from django.db.models import Q
import hashlib
import re
import json
from qiniu import Auth
access_key = "MDWzu5EOTAbqoJp5EGxGcdksEcSLnixxAcGsbv2v"
secret_key = "IujhqwUXdusrrLYooPA4WZdJtS7RR6r65TALg2p_"
bucket_name = "weiliao"
pwdfix = "weimi"
photoCount = 43
photoUrl = "http://7xl0k3.com1.z0.glb.clouddn.com/photo"

def safestr(str):
    str = str.replace("\r", " ")
    str = str.replace("\t", " ")
    str = str.replace("\n", " ")
    str = str.replace("\\", "\\\\")
    str = str.replace("\"", "\\\"")
    return str

# 通过uid 和 pwd 获取一个用户 没有返回None
def queryUser(uid, pwd):
    try:
        pwd = hashlib.new("md5", pwd + pwdfix).hexdigest()
        user = User.objects.get(uid = uid, pwd = pwd)
    except:
        return None
    return user

# 通过uid 和 pwd 注册一个用户 返回None表示  uid已被注册, -1 为 服务器发生错误
def registerUser(uid, pwd):
    try:
        user = User.objects.get(uid = uid)
    except:
        try:
            user = User()
            user.uid = uid
            user.name = uid
            count = User.objects.count()
            photo = photoUrl + (str)(count % photoCount + 1) + ".jpg"
            user.photo = photo
            user.pwd = hashlib.new("md5", pwd + pwdfix).hexdigest()
            user.access_token = hashlib.new("md5", uid + pwdfix + user.pwd).hexdigest()
            user.save()
            return user
        except:
            return -1
    return None

# 参数 text(
# 聊天内容,文字消息为:消息内容; gif表情消息为:gif表情对应的图片名
# 称 名称;语音,图片消息为:资源的url
# )
# type(消息类型)
# access_token
# to_user(接收者uid)
# 返回:-1, 登录失效, -2, to_user不存在, None 服务器发生错误
def insertMessage(text, type, access_token, to_user):
    try:
        from_user = User.objects.get(access_token = access_token)
    except:
        return -1
    try:
        to_user = User.objects.get(uid = to_user)
    except:
        return -2
    try:
        if to_user.uid == from_user.uid:
            return -2
        message = Message()
        message.text = safestr(text)
        message.type = type
        message.to_user = to_user
        message.save()
        from_user.messgaes.add(message)
        from_user.save()
        return {"message" : message}
    except:
        return None

# 通过access_token 获得 消息id大于since_id的数据, 并且不多于 count 条
def queryNewMessages(since_id, access_token, count):
    try:
        user = User.objects.get(access_token = access_token)
    except:
        return -1
    try:
        if (int)(since_id) > 0:
            # 查找 id > since_id 并且由 user 接收的 message 最近的 count 条
            messages_to_user = Message.objects.filter(to_user = user, id__gt = since_id).order_by("id")[0 : count]
            # 查找 id > since_id 并且由 user 发出的 message 最近的 count 条
            messages_from_user = user.messgaes.filter(id__gt = since_id).order_by("id")[0 : count]
            messages = set()
            for message in messages_to_user:
                messages.add(message)
            for message in messages_from_user:
                messages.add(message)
            messages = sorted(list(messages), key=lambda m1:m1.id)[0 : count]

            return {"messages" : messages}
        else:
            # 查找 由 user 接收的 message 最近的 count 条
            messages_to_user = Message.objects.filter(to_user = user).order_by("-id")[0 : count]
            # 查找 由 user 发出的 message 最近的 count 条
            messages_from_user = user.messgaes.all().order_by("-id")[0 : count]
            messages = set()
            for message in messages_to_user:
                messages.add(message)
            for message in messages_from_user:
                messages.add(message)
            messages = sorted(list(messages), key=lambda m1:-m1.id)[0 : count]

            return {"messages" : messages}


    except:
        return None

# 通过access_token 获得 消息id小于max_id的数据, 并且不多于 count 条
def queryOldMessages(max_id, access_token, count):
    try:
        user = User.objects.get(access_token = access_token)
    except:
        return -1
    try:
        # 查找 id < max_id 并且由 user 接收的 message 最近的 count 条
        messages_to_user = Message.objects.filter(to_user = user, id__lt = max_id).order_by("-id")[0 : count]
        # 查找 id < max_id 并且由 user 发出的 message 最近的 count 条

        messages_from_user = user.messgaes.filter(id__lt = max_id).order_by("-id")[0 : count]
        messages = set()
        for message in messages_to_user:
            messages.add(message)
        for message in messages_from_user:
            messages.add(message)
        messages = sorted(list(messages), key=lambda m1:-m1.id)[0 : count]

        return {"messages" : messages}
    except:
        return None


# 参数 text(
# text(状态内容)
# access_token
# pics(图片)
# 返回:-1, 登录失效, -2, to_user不存在, None 服务器发生错误
def insertStatus(text, access_token, pics):
    try:
        from_user = User.objects.get(access_token = access_token)
    except:
        return -1
    try:
        status = Status()
        status.text = safestr(text)
        status.pics = " ".join(pics)
        status.from_user = from_user
        status.save()
        return {"status" : status}
    except:
        return None


# 通过access_token 获得 status id大于since_id的数据, 并且不多于 count 条
def queryNewStatuses(since_id, access_token, count):
    try:
        user = User.objects.get(access_token = access_token)
    except:
        return -1
    try:
        if (int)(since_id) > 0:
            # 查找 id > since_id 并且由 user 发出的 status 或者 user 的好友发出的 status (最近的 count 条)
            statuses = Status.objects.filter(Q(from_user = user) | Q(from_user__in = user.friends.all()) ,id__gt = since_id).order_by("id")[0 : count]
            for status in statuses:
                status.pics = picsWithText(status.pics)
            # id大的在前
            statuses = sorted(statuses, key=lambda s1:-s1.id)[0 : count]
            return {"statuses" : statuses}
        else:
            # 查找 由 user 发出的 status 或者 user 的好友发出的 status (最近的 count 条)
            statuses = Status.objects.filter(Q(from_user = user) | Q(from_user__in = user.friends.all())).order_by("-id")[0 : count]
            for status in statuses:
                status.pics = picsWithText(status.pics)
            # id大的在前
            statuses = sorted(statuses, key=lambda s1:-s1.id)[0 : count]
            return {"statuses" : statuses}
    except:
        return None

# 通过access_token 获得 status id大于since_id的数据, 并且不多于 count 条
def queryOldStatuses(max_id, access_token, count):
    try:
        user = User.objects.get(access_token = access_token)
    except:
        return -1
    try:
        # 查找 id > since_id 并且由 user 发出的 status  或者 user 的好友发出的 status 最近的 count 条
        statuses = Status.objects.filter(Q(from_user = user) | Q(from_user__in =  user.friends.all()), id__lt = max_id).order_by("-id")[0 : count]
        for status in statuses:
            status.pics = picsWithText(status.pics)
        # id大的在前
        statuses = sorted(statuses, key=lambda s1:-s1.id)[0 : count]
        return {"statuses" : statuses}
    except:
        return None

# 处理图片(pics) 数组
def picsWithText(text):
    arr = text.split(" ")
    pics = list()
    regex = re.compile(
        r'^(?:http|ftp)s?://'
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
        r'localhost|'
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
        r'(?::\d+)?'
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    for pic in arr:
        if regex.match(pic):
            pics.append(pic)
    return pics

# 添加一条评论
def insertComment(text, access_token, s_id):
    try:
        from_user = User.objects.get(access_token = access_token)
    except:
        return -1
    try:
        status = Status.objects.get(id = s_id)
    except:
        return -2
    try:
        comment = Comment()
        comment.text = safestr(text)
        comment.status = status
        comment.from_user = from_user
        comment.save()
        return {"comment" : comment}
    except:
        return None

# 获取一条状态的所有评论
def queryComments(s_id):
    try:
        status = Status.objects.get(id = s_id)
    except:
        return -2
    try:
        comments = status.comment_set.all().order_by('-id')
        return {"comments" : comments}
    except:
        return None

# 请求添加朋友
def addFriend(text, access_token, to_user):
    try:
        from_user = User.objects.get(access_token = access_token)
    except:
        return -1
    try:
        to_user = User.objects.get(uid = to_user)
    except:
        return -2
    try:
        if to_user.uid == from_user.uid:
            return -3
        if from_user in to_user.friends.all():
            return -4
        # 防止请求重复发
        newfirends = from_user.newfriends.filter(to_user = to_user, status = 0)
        if newfirends.count() != 0:
            return -5
        newfirends = to_user.newfriends.filter(to_user = from_user, status = 0)
        if newfirends.count() != 0:
            return -6
        newfirend = Newfriend()
        newfirend.text = safestr(text)
        newfirend.to_user = to_user
        newfirend.save()
        from_user.newfriends.add(newfirend)
        from_user.save()
        return {"newfirend" : newfirend}
    except:
        return None

# 处理一个好友请求
def dowithAddFriend(f_id, access_token, result):
    try:
        to_user = User.objects.get(access_token = access_token)
    except:
        return -1
    try:
        newfirend = Newfriend.objects.get(id = f_id)
    except:
        return -2
    try:
        if newfirend.to_user.uid != to_user.uid or newfirend.status != 0:
            return -2
        newfirend.status = result
        newfirend.save()
        if result == 2:
            from_user = newfirend.user_set.all().first()
            to_user.friends.add(from_user)
            to_user.save()
            insertMessage("我已经同意你的好友请求了,开始对话吧!", 0, access_token, from_user.uid)
        return {"newfirend" : newfirend}
    except:
        return None

# 删除一个好友
def deleteFriend(to_user, access_token):
    try:
        from_user = User.objects.get(access_token = access_token)
    except:
        return -1
    try:
        to_user = User.objects.get(uid = to_user)
    except:
        return -2
    try:
        if to_user.uid == from_user.uid:
            return -3
        if from_user not in to_user.friends.all():
            return -4
        from_user.friends.remove(to_user)
        from_user.save()
        return {"from_user" : from_user}
    except:
        return None
# 获取所有的好友请求
def newFriends(access_token):
    try:
        user = User.objects.get(access_token = access_token)
    except:
        return -1
    try:
        newfriends = Newfriend.objects.filter(to_user = user, status = 0)
        return {"newfriends" : newfriends}
    except:
        return None

# 获取好友列表
def queryFriendList(access_token):
    try:
        user = User.objects.get(access_token = access_token)
    except:
        return -1
    try:
        friendlist = user.friends.all().order_by("-name", "-uid")
        return {"friendlist" : friendlist}
    except:
        return None
# 搜索陌生人
def querySearch(access_token, key, page):
    try:
        user = User.objects.get(access_token = access_token)
    except:
        return -1
    try:
        myfriend_uid = list()
        myfriend_uid.append(user.uid)
        myfriend = user.friends.all()
        for f in myfriend:
            myfriend_uid.append(f.uid)
        users = User.objects.filter((Q(uid__icontains = key) | Q(name__icontains = key)) & ~Q(uid__in = myfriend_uid))[page * 10 : (page + 1) * 10]
        return {"users" : users}
    except:
        return None

# 获取用户信息

def queryUserInfo(uid, access_token):
    try:
        user = User.objects.get(access_token = access_token)
    except:
        return -1
    try:
        to_user = User.objects.get(uid = uid)
        isfriend = 0
        if to_user in user.friends.all():
            isfriend = 1
        return {"user" : to_user, "isfriend" : isfriend}
    except:
        return -2

#  更新用户信息 "phton",
#     name
#     "age":
#     "sex":
#     "birthday":
#     "city":
def updateUserInfo(access_token, name, age, sex, birthday, city):
    try:
        user = User.objects.get(access_token = access_token)
    except:
        return -1
    try:
        user.name = safestr(name)
        user.age = age
        user.sex = sex
        user.birthday = birthday
        user.city = safestr(city)
        user.save()
        return {"user" : user}
    except:
        return None

#  更新用户密码
def updateUserPwd(access_token, pwd, oldpwd):
    try:
        user = User.objects.get(access_token = access_token)
    except:
        return -1
    try:
        if user.pwd != hashlib.new("md5", oldpwd + pwdfix).hexdigest():
            return -2
        user.pwd = hashlib.new("md5", pwd + pwdfix).hexdigest()
        user.access_token = hashlib.new("md5", user.uid + pwdfix + user.pwd).hexdigest()
        user.save()
        return {"user" : user}
    except:
        return None
# 更新用户头像
def updateUserPhoto(access_token, photo):
    try:
        user = User.objects.get(access_token = access_token)
    except:
        return -1
    try:
        user.photo = photo
        user.save()
        return {"user" : user}
    except:
        return None

# 获得七牛上传凭证 key 文件名
def getQiniu_token(key):
    q = Auth(access_key, secret_key)
    token = q.upload_token(bucket_name, key)
    return {"token" : token}