from django.db import models
from django.contrib.auth.models import User

#Extend user class
class ExtendUser(models.Model):
	""" extend user class to help out in templates etc """
	
	user = models.OneToOneField(User)
	
	def __unicode__(self):
		return "Extend of %s" % self.user
		
	#returns current character
	def current_character(self):
		return self.user.character_set.get(alive=True).region.name
