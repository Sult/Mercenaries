from django.db import models

from characters.models import Character

from collections import namedtuple


class MailFolder(models.Model):
	""" folders to hold and sort messages 
		Inbox, sent and thrash
	"""
	
	character = models.ForeignKey(Character)
	
	name = models.CharField(max_length=31)
	locked = models.BooleanField()

	class Meta:
		unique_together = ['character', 'name']
	
	
	def __unicode__(self):
		return "%s: %s" % (self.character, self.name)
	
	
	@staticmethod
	def create_standard_folders(character):
		folders = ["inbox", "archive", "sent", "trash"]
		
		for folder in folders:
			new_folder = MailFolder(
				character=character,
				name=folder,
				locked=True,
			)
			new_folder.save()
	
	
	#order folders for mail view
	@staticmethod
	def order_folders(character):
		folders = MailFolder.objects.filter(character=character)
		
		list_folders = []
		
		for folder in folders:
			list_folders.append(folder)
		
		return list_folders
		
	
	
		
		


#basic message
class Mail(models.Model):
	""" message composition """
	
	PLAYER = "player"
	PROMOTION = "promotion"
	CRIME = "crime"
	ALLIANCE = "alliance"
	MAILCATEGORIES = (
		(PLAYER, "player"),
		(PROMOTION, "promotion"),
		(CRIME, "crime"),
		(ALLIANCE, "alliance"),
	)
	
	folder = models.ForeignKey(MailFolder)
	
	sender = models.ForeignKey(Character, related_name="+")
	to = models.ForeignKey(Character, related_name="+")
	read = models.BooleanField(default=False)
	sent_at = models.DateTimeField(auto_now_add=True)
	category = models.CharField(max_length=15, choices=MAILCATEGORIES)
	subject = models.CharField(max_length=127)
	body = models.TextField()
	
	def __unicode__(self):
		return "%s: %s: %s" % (self.to, self.subject, self.read)

	
	def reply_format(self):
		message = self.body
		message = "> " + message
		message = message.replace("\r\n", "\r\n> ")
		send_information = "\r\n\r\n> To: %s\r\n> From: %s\r\n> Date: %s\r\n>\r\n" % (self.to, self.sender, self.view_sent_at())
		message = send_information + message
		return message
		
	
	#format sent_at date
	def view_sent_at(self):
		return self.sent_at.strftime("%H:%M %d-%m-%Y")


#class Messagebox(models.Model):
	#""" holds incomming messages """
	
	#character = models.ForeignKey(Character, related_name"+")
	




	


