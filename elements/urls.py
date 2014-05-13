from django.conf.urls import patterns, url

from elements import views

urlpatterns = patterns('',
	#User actions
	url(r'^short_job/$', views.short_job, name='short job'),
	url(r'^medium_job/$', views.medium_job, name='medium job'),
	
	url(r'^market/$', views.market, name='market'),
)
