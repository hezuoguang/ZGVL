# coding:utf-8
from django.shortcuts import render, render_to_response, HttpResponse

from api.function import *

from api.models import *
defaultCount = 40

# Create your views here.
# API文档
def doc(request):
    return render_to_response("doc/doc.html", {})

# 登录处理 POST方式, 参数 uid, pwd, pwd须进行MD5加密
def login(request):
    if request.method == "POST":
        try:
            uid = request.POST["uid"]
            pwd = request.POST["pwd"]
        except:
            return error("请求参数不正确")
        user = queryUser(uid, pwd)
        if user == None:
            return error("用户名或密码错误")
        context = dict()
        context["uid"] = user.uid;
        context["name"] = user.name
        context["photo"] = user.photo;
        context["access_token"] = user.access_token
        return render_to_response("login.json", context, content_type = 'application/json')
    else:
        return error("请求方式不正确,应使用POST")
# 注册处理 POST方式, 参数 uid, pwd, pwd须进行MD5加密
def register(request):
    if request.method == "POST":
        try:
            uid = request.POST["uid"]
            pwd = request.POST["pwd"]
            if len(pwd) < 6 or len(pwd) > 64:
                return error("密码长度不符合要求")
            if len(uid) < 6 or len(uid) > 16:
                return error("用户名长度不符合要求")
        except:
            return error("请求参数不正确")
        user = registerUser(uid, pwd)
        if user == None:
            return error("注册失败, 用户名已被注册")
        elif user == -1:
            return error("注册失败, 请稍后再试")
        return render_to_response("register.json", {}, content_type = "application/json")
    else:
        return error("请求方式不正确,应使用POST")

# 发送一条消息 POST方式,
# 参数 text(
# 聊天内容,文字消息为:消息内容; gif表情消息为:gif表情对应的图片名
# 称 名称;语音,图片消息为:资源的url
# )
# type(消息类型) (0, "文本消息"),(1, "gif表情消息"),(2, "图片消息"),(3, "语音消息")
# access_token
# to_user(接收者uid)
def chat_upload(request):
    if request.method == "POST":
        try:
            # 还须细化 为语音和图片消息时 并未对参数的进行严格的判定(url)
            text = request.POST["text"]
            access_token = request.POST["access_token"]
            to_user = request.POST["to_user"]
            type = request.POST["type"]
            type = (int)(type)
            if type < 0 or type > 3:
                type = 0
        except:
            return error("请求参数不正确")
        context = insertMessage(text, type, access_token, to_user)
        if context == -1:
            return error("登录失效, 请重新登录")
        elif context == -2:
            return error("目的用户不存在")
        elif context == None:
            return error("服务器发生错误")
        return render_to_response("chat/upload.json", context, content_type = "application/json")
    else:
        return error("请求方式不正确,应使用POST")
# 获得新的message POST方式,
# 参数 access_token, since_id, count
# 通过access_token 获得 消息id大于since_id的数据, 并且不多于 count 条
def chat_newmessages(request):
    if request.method == "POST":
        try:
            since_id = request.POST["since_id"]
            access_token = request.POST["access_token"]
            count = defaultCount
            if request.POST.has_key("count"):
                count = (int)(request.POST["count"])
            if count <= 0:
                count = 1
            elif count > defaultCount:
                count = defaultCount
        except:
            return error("请求参数不正确")
        context = queryNewMessages(since_id, access_token, count)
        if context == -1:
            return error("登录失效, 请重新登录")
        elif context == None:
            return error("服务器发生错误")
        return render_to_response("chat/messages.json", context, content_type = "application/json")
    else:
        return error("请求方式不正确,应使用POST")

# 获得旧的message POST方式,
# 参数 access_token, max_id, count
# 通过access_token 获得 消息id < max_id的数据, 并且不多于 count 条
def chat_oldmessages(request):
    if request.method == "POST":
        try:
            max_id = request.POST["max_id"]
            access_token = request.POST["access_token"]
            count = defaultCount
            if request.POST.has_key("count"):
                count = (int)(request.POST["count"])
            if count <= 0:
                count = 1
            elif count > defaultCount:
                count = defaultCount
        except:
            return error("请求参数不正确")
        context = queryOldMessages(max_id, access_token, count)
        if context == -1:
            return error("登录失效, 请重新登录")
        elif context == None:
            return error("服务器发生错误")
        return render_to_response("chat/messages.json", context, content_type = "application/json")
    else:
        return error("请求方式不正确,应使用POST")


# 发送一条状态 POST方式,
# 参数 text(状态内容)
# pics(图片地址, 数组)
# access_token(发送者)
def status_upload(request):
    if request.method == "POST":
        try:
            text = request.POST["text"]
            access_token = request.POST["access_token"]
            pics = list()
            # 还须细化  并未对参数的进行严格的判定(url)
            if request.POST.has_key("pics[]"):
                pics = request.POST.getlist('pics[]')
                print pics
                if len(pics) > 9:
                    return error("图片数量不能多于9张")
        except:
            return error("请求参数不正确")
        context = insertStatus(text,access_token, pics)
        if context == -1:
            return error("登录失效, 请重新登录")
        elif context == None:
            return error("服务器发生错误")
        return render_to_response("status/upload.json", context, content_type = "application/json")
    else:
        return error("请求方式不正确,应使用POST")

# 获得新的status POST方式,
# 参数 access_token, since_id, count
# 通过access_token 获得 status id大于since_id的数据, 并且不多于 count 条
def status_newstatuses(request):
    if request.method == "POST":
        try:
            since_id = request.POST["since_id"]
            access_token = request.POST["access_token"]
            count = defaultCount
            if request.POST.has_key("count"):
                count = (int)(request.POST["count"])
            if count <= 0:
                count = 1
            elif count > defaultCount:
                count = defaultCount
        except:
            return error("请求参数不正确")
        context = queryNewStatuses(since_id, access_token, count)
        if context == -1:
            return error("登录失效, 请重新登录")
        elif context == None:
            return error("服务器发生错误")
        return render_to_response("status/statuses.json", context, content_type = "application/json")
    else:
        return error("请求方式不正确,应使用POST")

# 获得旧的status POST方式,
# 参数 access_token, max_id, count
# 通过access_token 获得 status id < max_id的数据, 并且不多于 count 条
def status_oldstatuses(request):
    if request.method == "POST":
        try:
            max_id = request.POST["max_id"]
            access_token = request.POST["access_token"]
            count = defaultCount
            if request.POST.has_key("count"):
                count = (int)(request.POST["count"])
            if count <= 0:
                count = 1
            elif count > defaultCount:
                count = defaultCount
        except:
            return error("请求参数不正确")
        context = queryOldStatuses(max_id, access_token, count)
        if context == -1:
            return error("登录失效, 请重新登录")
        elif context == None:
            return error("服务器发生错误")
        return render_to_response("status/statuses.json", context, content_type = "application/json")
    else:
        return error("请求方式不正确,应使用POST")


# 发送一条评论 POST方式,
# 参数 text(评论内容)
# access_token
# s_id(status id)
def comment_upload(request):
    if request.method == "POST":
        try:
            text = request.POST["text"]
            access_token = request.POST["access_token"]
            s_id = request.POST["s_id"]
        except:
            return error("请求参数不正确")
        context = insertComment(text, access_token, s_id)
        if context == -1:
            return error("登录失效, 请重新登录")
        elif context == -2:
            return error("该状态不存在")
        elif context == None:
            return error("服务器发生错误")
        return render_to_response("comment/upload.json", context, content_type = "application/json")
    else:
        return error("请求方式不正确,应使用POST")

# 获取一条状态的所有评论 POST方式,
# s_id(status id)
def comment_comments(request):
    if request.method == "POST":
        try:
            s_id = request.POST["s_id"]
        except:
            return error("请求参数不正确")
        context = queryComments(s_id)
        if context == -2:
            return error("该状态不存在")
        elif context == None:
            return error("服务器发生错误")
        return render_to_response("comment/comments.json", context, content_type = "application/json")
    else:
        return error("请求方式不正确,应使用POST")

# 请求添加好友 POST方式,
# to_user(接收者uid)
# text(请求说明)
# access_token
def friend_addfriend(request):
    if request.method == "POST":
        try:
            text = request.POST["text"]
            access_token = request.POST["access_token"]
            to_user = request.POST["to_user"]
        except:
            return error("请求参数不正确")
        context = addFriend(text, access_token, to_user)
        if context == -1:
            return error("登录失效, 请重新登录")
        elif context == -2:
            return error("添加的用户不存在")
        elif context == -3:
            return error("不能添加自己为好友")
        elif context == -4:
            return error("对方已经是你好友了")
        elif context == -5:
            return error("请求已发出无需重复请求")
        elif context == -6:
            return error("对方已对你发出好友请求,同意其请求即可")
        elif context == None:
            return error("服务器发生错误")
        return render_to_response("friend/addfriend.json", context, content_type = "application/json")
    else:
        return error("请求方式不正确,应使用POST")

# 处理添加好友请求 POST方式,
# f_id(好友请求消息id)
# access_token
# result (处理结果)(1, "拒绝"),(2, "同意")
def friend_dowithrequest(request):
    if request.method == "POST":
        try:
            access_token = request.POST["access_token"]
            f_id = request.POST["f_id"]
            result = request.POST["result"]
            result = (int)(result)
            if result != 1 and result != 2:
                result = 1
        except:
            return error("请求参数不正确")
        context = dowithAddFriend(f_id, access_token, result)
        if context == -1:
            return error("登录失效, 请重新登录")
        elif context == -2:
            return error("该请求不存在")
        elif context == -3:
            return error("不能添加自己为好友")
        elif context == -4:
            return error("对方已经是你好友了")
        elif context == -5:
            return error("请求已发出无需重复请求")
        elif context == -6:
            return error("对方已对你发出好友请求,同意其请求即可")
        elif context == None:
            return error("服务器发生错误")
        return render_to_response("friend/addfriend.json", context, content_type = "application/json")
    else:
        return error("请求方式不正确,应使用POST")
# 删除一个好友
def friend_deletefriend(request):
    if request.method == "POST":
        try:
            access_token = request.POST["access_token"]
            to_user = request.POST["to_user"]
        except:
            return error("请求参数不正确")
        context = deleteFriend(to_user, access_token)
        if context == -1:
            return error("登录失效, 请重新登录")
        elif context == -2:
            return error("欲删除的用户不存在")
        elif context == -3:
            return error("不能删除自己")
        elif context == -4:
            return error("对方还不是你好友")
        elif context == None:
            return error("服务器发生错误")
        return render_to_response("friend/addfriend.json", context, content_type = "application/json")
    else:
        return error("请求方式不正确,应使用POST")

# 获取所有未处理的好友请求
def friend_newfriends(request):
    if request.method == "POST":
        try:
            access_token = request.POST["access_token"]
        except:
            return error("请求参数不正确")
        context = newFriends(access_token)
        if context == -1:
            return error("登录失效, 请重新登录")
        elif context == None:
            return error("服务器发生错误")
        return render_to_response("friend/newfriends.json", context, content_type = "application/json")
    else:
        return error("请求方式不正确,应使用POST")

# 获取好友列表
def friend_friendlist(request):
    if request.method == "POST":
        try:
            access_token = request.POST["access_token"]
        except:
            return error("请求参数不正确")
        context = queryFriendList(access_token)
        if context == -1:
            return error("登录失效, 请重新登录")
        elif context == None:
            return error("服务器发生错误")
        return render_to_response("friend/friendlist.json", context, content_type = "application/json")
    else:
        return error("请求方式不正确,应使用POST")
# 搜索陌生人
def friend_search(request):
    if request.method == "POST":
        try:
            access_token = request.POST["access_token"]
            key = request.POST["key"]
            page = request.POST["page"]
            page = (int)(page)
        except:
            return error("请求参数不正确")
        context = querySearch(access_token, key, page)
        if context == -1:
            return error("登录失效, 请重新登录")
        elif context == None:
            return error("服务器发生错误")
        return render_to_response("friend/users.json", context, content_type = "application/json")
    else:
        return error("请求方式不正确,应使用POST")

# 获取用户信息, uid
def user_userinfo(request):
    if request.method == "POST":
        try:
            uid = request.POST["uid"]
            access_token = request.POST["access_token"]
        except:
            return error("请求参数不正确")
        context = queryUserInfo(uid, access_token)
        if context == -1:
            return error("登录失效, 请重新登录")
        elif context == -2:
            return error("用户不存在")
        elif context == None:
            return error("服务器发生错误")
        return render_to_response("user/userinfo.json", context, content_type = "application/json")
    else:
        return error("请求方式不正确,应使用POST")

# 更新用户信息, access_token
def user_updateuserinfo(request):
    if request.method == "POST":
        try:
            access_token = request.POST["access_token"]
            name = request.POST["name"]
            age = request.POST["age"]
            sex = request.POST["sex"]
            birthday = request.POST["birthday"]
            city = request.POST["city"]
            if len(city) <= 0 or len(name) <= 0 or len(age) <= 0 or len(sex) <= 0 or len(birthday) <= 0:
                return error("请求参数不正确")
        except:
            return error("请求参数不正确")
        context = updateUserInfo(access_token, name, age, sex, birthday, city)
        if context == -1:
            return error("用户不存在")
        elif context == None:
            return error("服务器发生错误")
        return render_to_response("user/userinfo.json", context, content_type = "application/json")
    else:
        return error("请求方式不正确,应使用POST")

# 更新用户密码, access_token, pwd oldpwd
def user_updateuserpwd(request):
    if request.method == "POST":
        try:
            access_token = request.POST["access_token"]
            pwd = request.POST["pwd"]
            oldpwd = request.POST["oldpwd"]
            if len(pwd) < 6 or len(pwd) > 64:
                return error("密码长度不能小于6")
        except:
            return error("请求参数不正确")
        context = updateUserPwd(access_token, pwd, oldpwd)
        if context == -1:
            return error("用户不存在")
        elif context == -2:
            return error("旧密码不符,修改失败")
        elif context == None:
            return error("服务器发生错误")
        return render_to_response("user/userinfo.json", context, content_type = "application/json")
    else:
        return error("请求方式不正确,应使用POST")
# 更新用户头像, access_token, photo
def user_updateuserphoto(request):
    if request.method == "POST":
        try:
            access_token = request.POST["access_token"]
            photo = request.POST["photo"]
        except:
            return error("请求参数不正确")
        context = updateUserPhoto(access_token, photo)
        if context == -1:
            return error("用户不存在")
        elif context == None:
            return error("服务器发生错误")
        return render_to_response("user/userinfo.json", context, content_type = "application/json")
    else:
        return error("请求方式不正确,应使用POST")

def qiniu_token(request):
    if request.method == "POST":
        try:
            key = request.POST["fileName"]
        except:
            return error("请求参数不正确")
        context = getQiniu_token(key)
        if context == None:
            return error("服务器发生错误")
        return render_to_response("qiniu/token.json", context, content_type = "application/json")
    else:
        return error("请求方式不正确,应使用POST")

def error(message):
    return render_to_response("error.json", {"message" : message}, content_type = 'application/json')