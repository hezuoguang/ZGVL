#coding:utf-8
from django.conf.urls import patterns, include, url

from api.views import *



urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'zgvl.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),


    # 登录
    url(r'^login.json', login),
    # 注册
    url(r'^register.json', register),

    # 发送一条消息
    url(r'^chat/upload.json', chat_upload),
    # 获取新的消息, 消息的id大于since_id, 默认最多获取40条
    url(r'^chat/newmessages.json', chat_newmessages),
    # 获取旧的消息, 消息的id小于max_id 默认最多获取40条
    url(r'^chat/oldmessages.json', chat_oldmessages),

    # 发送一条状态
    url(r'^status/upload.json', status_upload),
    # 获取新的状态, 消息的id大于since_id, 默认最多获取40条
    url(r'^status/newstatuses.json', status_newstatuses),
    # 获取旧的状态, 消息的id小于max_id 默认最多获取40条
    url(r'^status/oldstatuses.json', status_oldstatuses),

    # 发送一条评论
    url(r'^comment/upload.json', comment_upload),
    # 获取一条状态的所有评论
    url(r'^comment/comments.json', comment_comments),

    # 请求添加好友
    url(r'^friend/addfriend.json', friend_addfriend),
    # 处理一个好友请求
    url(r'^friend/dowithrequest.json', friend_dowithrequest),
    # 删除一个好友
    url(r'^friend/deletefriend.json', friend_deletefriend),
    # 获取所有未处理的好友请求
    url(r'^friend/newfriends.json', friend_newfriends),
    # 获取好友列表
    url(r'^friend/friendlist.json', friend_friendlist),
    # 搜索陌生人
    url(r'^friend/search.json', friend_search),

    # 获取用户信息
    url(r'^user/userinfo.json', user_userinfo),
    # 更新用户信息
    url(r'^user/updateuserinfo.json', user_updateuserinfo),
    # 更新用户密码
    url(r'^user/updateuserpwd.json', user_updateuserpwd),
    # 更新用户头像
    url(r'^user/updateuserphoto.json', user_updateuserphoto),

    # 获得七牛上传凭证
    url(r'^qiniu/token.json', qiniu_token),

    # 接口文档
    url(r'^doc', doc),
    url(r'^', doc),

)
# from django.contrib.staticfiles.urls import staticfiles_urlpatterns
# urlpatterns += staticfiles_urlpatterns()