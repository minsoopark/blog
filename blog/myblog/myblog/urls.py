from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'myblog.views.home', name='home'),
    # url(r'^myblog/', include('myblog.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^$', 'blog.views.main_page'),
    url(r'^blog/$', 'blog.views.index'),
    url(r'^blog/page/(?P<page>\d+)/$', 'blog.views.index'),
    url(r'^blog/entry/(?P<entry_id>\d+)/$', 'blog.views.read'),
    url(r'^blog/write/post/$', 'blog.views.write_form'),
    url(r'^blog/add/post/$', 'blog.views.add_post'),
    url(r'^blog/add/comment/$', 'blog.views.add_comment'),
    url(r'^blog/add/user/$', 'blog.views.add_user'),
    url(r'^accounts/profile/$', 'blog.views.profile'),
    url(r'^login/$', 'django.contrib.auth.views.login'),
    url(r'^logout/$', 'blog.views.logout_page'),
    url(r'^join/$', 'blog.views.join_form'),
    url(r'^admin/', include(admin.site.urls)),
)
