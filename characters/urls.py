from django.conf.urls import patterns, url

from characters import views

urlpatterns = patterns('',
	url(r'^$', views.index, name='index'),
	url(r'^character/$', views.character, name='character'),
	url(r'^garage/$', views.garage, name='garage'),
	url(r'^gun_depot/$', views.gun_depot, name='gun depot'),
	url(r'^contraband/$', views.contraband, name='contraband'),
	
	#jobs
	url(r'^long_job/$', views.long_job, name='long job'),
	url(r'^group_crime/$', views.group_crime, name='group crime'),
	url(r'^travel/$', views.travel, name='travel'),
	url(r'^blood/$', views.blood, name='blood'),
	url(r'^race/$', views.race, name='race'),
	url(r'^kill/$', views.kill, name='kill'),
	url(r'^bullet_deal/$', views.bullet_deal, name='bullet deal'),
	
)
