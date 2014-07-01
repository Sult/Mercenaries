from django.conf.urls import patterns, url

from elements import views

urlpatterns = patterns('',
	#User actions
	url(r'^short_job/$', views.short_job, name='short job'),
	url(r'^medium_job/$', views.medium_job, name='medium job'),
	
	#market
	url(r'^market/$', views.market, name='market'),
	url(r'^transport/$', views.transport, name='transport'),
	url(r'^travel_method/$', views.travel_method, name='travel method'),
	url(r'^housing/$', views.housing, name='housing'),
)
