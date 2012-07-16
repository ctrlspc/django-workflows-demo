'''
Created on Jul 15, 2012

@author: jasonmarshall
'''

from django.conf.urls import patterns, url



urlpatterns = patterns('tokens.views',
    # Examples:
    url(r'^$', 'home', name='home_view'),
    url(r'^create$', 'create', name='create_view'),
    url(r'^edit/(?P<token>\d+)$', 'edit', name='edit_view'),
    url(r'^submit/(?P<token>\d+)$', 'submit', name='submit_view'),
    url(r'^delete/(?P<token>\d+)$', 'delete', name='delete_view'),
    url(r'^approve/(?P<token>\d+)$', 'evaluate', {'approved':True}, name='approve_view'),
    url(r'^reject/(?P<token>\d+)$', 'evaluate', {'approved':False}, name='reject_view'),
    
)