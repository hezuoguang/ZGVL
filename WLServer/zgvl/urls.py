#coding:utf-8
from django.conf.urls import patterns, include, url

from django.contrib import admin

from api.views import doc
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'zgvl.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin', include(admin.site.urls)),
    url(r'^admin/', include(admin.site.urls)),
    # api路由
    url(r'^api/', include('api.urls')),

)
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns += staticfiles_urlpatterns()
urlpatterns += patterns('',
    # apidoc
    url(r'^', doc),
)