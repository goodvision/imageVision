from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'myLife.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$','myLife.views.index'),
    url(r'^page/pagenum=(\d)$','myLife.views.index'),
    url(r'^signin/$','myLife.views.signin'),
    url(r'^phone/',include('phone.urls')),
    url(r'^fileUp/','myLife.views.fileUp'),
    url(r'^download/filepath=([\s\S]*)$','myLife.views.fileDownload'),
    #url(r'^static/(?P<path>.*)$', 'django.views.static.serve',{'document_root': settings.STATIC_ROOT,'show_indexes': True }), 
)


if settings.DEBUG and not urlpatterns:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    
if not settings.DEBUG:
    urlpatterns += patterns('', url(r'^static/(?P.*)$', 'django.views.static.serve',{'document_root': settings.STATIC_ROOT}),
    )
    
