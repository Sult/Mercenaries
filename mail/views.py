from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.core.urlresolvers import reverse
from django.core.context_processors import csrf
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required

from mercs.decorators import still_alive
from mail.models import MailFolder, Mail
from mail.forms import MailForm
from mail.forms import get_actions, mail_actions, send_mail, mail_options
from mercs.helpers import sort_queryset_by_field



@login_required
@still_alive
def mail_folder(request, folder_name):
	character = request.user.character_set.get(alive=True)
	folder = get_object_or_404(MailFolder, name=folder_name, character=character)
	session = request.session
	
	if request.POST:
		mail_actions(request.POST, character)
	
	
	# sorting
	if request.GET:
		order_by = request.GET.get('order_by', "id")
		
		if session['order_by'] == order_by:
			if session['order_by_last']:
				session['order_by_last'] = False
			else:
				session['order_by_last'] = True
		else:
			session['order_by'] = order_by
			if not session['order_by_last']:
				session['order_by_last'] = True
		
		qs = Mail.objects.filter(folder=folder)
		mail_list = sort_queryset_by_field(qs, order_by, session["order_by_last"])
		
		print session['order_by_last']
		print session['order_by']
		
		
	else:
		mail_list = Mail.objects.filter(folder=folder).order_by('-sent_at')
	
	#paginator
	paginator = Paginator(mail_list, 15)
	page = request.GET.get("page")
	try:
		mails = paginator.page(page)
	except PageNotAnInteger:
		mails = paginator.page(1)
	except EmptyPage:
		mails = paginator.page(paginator.num_pages)
		
	actions = get_actions(folder)
		
	return render(request, "mail_overview.html", {"actions": actions, "mails": mails})




@login_required
@still_alive
def compose(request):
	character = request.user.character_set.get(alive=True)
	
	new_mail = MailForm()
	
	if request.POST:
		new_mail = MailForm(request.POST)
		
		if new_mail.is_valid():
			send_mail(request.POST, character)
			url = reverse('mail folder', kwargs={"folder_name": "inbox"})
			return HttpResponseRedirect(url)
	
	return render(request, "compose.html", {"new_mail": new_mail})
	
	

@login_required
@still_alive
def view_mail(request, mail_id):
	mail = get_object_or_404(Mail, pk=mail_id)
	
	#change mail to read
	if mail.read == False:
		mail.read = True
		mail.save()
	
	#mailoptions
	actions = [["reply", "reply"], ["forward", "forward"], ["archive", "move to archive"], ["trash", "move to trash"]]
	
	if request.POST:
		result = mail_options(request.POST, mail)
		if result:
			if type(result) is type({}):
				new_mail = MailForm(result)
				return render(request, "compose.html", {"new_mail": new_mail})
			else:
				url = reverse('mail folder', kwargs={"folder_name": "inbox"})
				return HttpResponseRedirect(url)
		else:
			return render(request, "mail.html", {"mail": mail, "actions": actions})
			
	return render(request, "mail.html", {"mail": mail, "actions": actions})
	
	
