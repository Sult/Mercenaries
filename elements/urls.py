from django.conf.urls import patterns, url

from elements import views

urlpatterns = patterns('',
	#User actions
	url(r'^short_job/$', views.short_job, name='short job'),
)
