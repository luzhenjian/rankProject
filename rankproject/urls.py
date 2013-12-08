from django.conf.urls import patterns, include, url
from rank.views import *
from forum.views import *
from news.views import *
from django.contrib.auth.decorators import login_required
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    #======admin====
    url(r'^admin/', include(admin.site.urls)),

    #======rank=====
    url(r'^$', 'rank.views.rank', name='rank'),
    url(r'^games/$', 'rank.views.games', name='game'),

    #======forum====
    url(r'^forum/$', 'forum.views.forum', name='forum'),
    url(r'^topic/(\d+)', 'forum.views.topic'),
    url(r'^thread/(\d+)', 'forum.views.thread'),
    url(r'^new_thread/(\d+)', 'forum.views.new_thread'),
    url(r'^new_post/(\d+)', 'forum.views.new_post'),
   
    #======twitter=== 
    url(r'^twitter/$', 'forum.views.twitter', name='twitter'),
    url(r'^about/$', 'forum.views.about', name='about'),

    #======news======
    url(r'^news/$', NewsListView.as_view(), name='news'),
    url(r'^news/submit/$', login_required(NewsCreateView.as_view()), name='submit'),
    url(r'^news/vote/$', 'news.views.vote', name='vote'),
    url(r'^comments/', include('django.contrib.comments.urls')),
    url(r'^comment/(\d+)', 'news.views.comment', name='comment'),

    #======account===
    url(r'^accounts/register/$', 'accounts.views.register', name="register"),  
    url(r'^accounts/login/$', 'accounts.views.login', name="login"),  
    url(r'^accounts/logout/$', 'accounts.views.logout', name="logout"), 
    
)
