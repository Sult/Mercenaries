from django import forms
from django.core.exceptions import ObjectDoesNotExist

from mail.models import MailFolder, Mail
from characters.models import Character


#create actions list for mail
def get_actions(folder):
	folders = ["inbox", "archive", "sent", "trash"]
	folders.remove(folder.name)
	actions = []
	
	if folder.name == "trash":
		actions.append(["delete", "delete"])
	
	elif folder.name == "sent":
		actions.append(["delete", "delete"])
		return actions
	
	else:
		actions.append(["read", "mark as read"])
		actions.append(["unread", "mark as unread"])
	
	#add folders to move to
	for folder in folders:
		actions.append(["%s" % folder, "move to %s" % folder])
	
	return actions


	

# handle mail actions
def mail_actions(postdata, character):
	folders = ["inbox", "archive", "sent", "trash"]
	action = postdata['action']
	mails = postdata.getlist('mails')
	
	#delete mail
	if action == "delete":
		for mail_id in mails:
			mail = Mail.objects.get(id=mail_id)
			mail.delete()
	
	#Move mail to folder
	elif action in folders:
		folder = MailFolder.objects.get(character=character, name=postdata['action'])
		for mail_id in mails:
			mail = Mail.objects.get(id=mail_id)
			mail.folder = folder
			mail.save()
	
	#mark mail as read
	elif action == "read":
		for mail_id in mails:
			mail = Mail.objects.get(id=mail_id)
			mail.read = True
			mail.save()
			
	#mark mail as unread
	elif action == "unread":
		for mail_id in mails:
			mail = Mail.objects.get(id=mail_id)
			mail.read = False
			mail.save()
	
	
	
#handle mail options like reply and forward
def mail_options(postdata, mail):
	option = postdata['options']
	folders = ["archive", "trash"]
	request = []
	
	#make up mail to reply
	if option == "reply":
		if mail.sender != None:
			to = mail.sender.name
			subject = "Re: " + mail.subject
			body = mail.reply_format()
			return {"to": to, "subject": subject, "body": body}
		else:
			return False
		
	#make up template to forward	
	elif option == "forward":
		subject = "Re: " + mail.subject
		body = mail.reply_format()
		return {"subject": subject, "body": body}
		
	#change folder of mail
	elif option in folders:
		mail.folder = MailFolder.objects.get(character=mail.to, name=option)
		mail.save()
		

	





class MailForm(forms.Form):
	to = forms.CharField(max_length=31, required=True)
	subject = forms.CharField(max_length=127, required=True)
	body = forms.CharField(
					widget=forms.Textarea, label='')


	def clean_to(self):
		to = self.cleaned_data['to']
		name = to.capitalize()

		try:
			recipient = Character.objects.get(name=name)		
		except ObjectDoesNotExist:
			raise forms.ValidationError("There is no player with that name.")
	
		return to
	
	
#send mail
def send_mail(postdata, character):
	name = postdata['to'].capitalize()
	to = Character.objects.get(name=name)
	
	new_mail = Mail(
		folder=MailFolder.objects.get(character=to, name="inbox"),
		category=Mail.PLAYER,
		to=to,
		sender=character,
		subject=postdata['subject'],
		body=postdata['body'],
	)
	new_mail.save()
	
	send_mail = Mail(
		folder=MailFolder.objects.get(character=character, name="sent"),
		category=Mail.PLAYER,
		to=to,
		read=True,
		sender=character,
		subject=postdata['subject'],
		body=postdata['body'],
	)
	send_mail.save()
	



