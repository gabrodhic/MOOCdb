from django.conf.urls import patterns, include, url
from django.contrib import admin
from foundary.views import CodeView,CommentView
from django.views.decorators.csrf import csrf_exempt
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'foundary.views.home', name='home'),
    #url(r'^get_log/$', 'foundary.views.get_log', name='get_log'),
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('foundary.views',
    url(r'^ajax/like/$', 'likeit', name='like'),
    url(r'^ajax/codes/$', csrf_exempt(CodeView.as_view()), name='codes'),
    url(r'^ajax/comments/$', csrf_exempt(CommentView.as_view()), name='comments'),
)
