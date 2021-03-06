from django.conf.urls import patterns, include, url



from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'usingWorkflows.views.home', name='home'),
    # url(r'^usingWorkflows/', include('usingWorkflows.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^token/', include('tokens.urls')),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login', name='login_view'),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout',{'next_page':'/token/'}, name='logout_view'),
)
