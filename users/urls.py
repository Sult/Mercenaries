from django.conf.urls import patterns, url

from users import views

urlpatterns = patterns('',
	#Authentication urls
	url(r'^login/$', views.login_user, name='login_user'),
	url(r'^logout/$', views.logout, name='logout'),
	url(r'^register/$', views.register_user, name='register_user'),
)

