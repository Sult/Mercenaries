from django.conf.urls import patterns, include, url
from django.conf import settings

#from django.contrib import admin
#admin.autodiscover()


urlpatterns = patterns('',

	#url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('users.urls')),
    url(r'^', include('characters.urls')),
    url(r'^', include('elements.urls')),
    url(r'^', include('mail.urls')),
)

if settings.DEBUG:
	urlpatterns += patterns('django.views.static',
		(r'media/(?P<path>.*)', 'serve', {'document_root': settings.MEDIA_ROOT}),
	)
