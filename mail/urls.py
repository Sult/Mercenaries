from django.conf.urls import patterns, url

from mail import views

urlpatterns = patterns('',
	#communications
	##Mail
	url(r'^mail/folder/(?P<folder_name>\w+)/$', views.mail_folder, name="mail folder"),
	url(r'^mail/compose/$', views.compose, name="compose"),
	url(r'^mail/(?P<mail_id>\d+)/$', views.view_mail, name="view mail"),
)
