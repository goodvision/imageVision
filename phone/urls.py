from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    
    url(r'^$','phone.views.first_phone'),
    url(r'^all/$','phone.views.all'),
)
