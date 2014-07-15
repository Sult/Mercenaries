from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.core.context_processors import csrf
from django.core.exceptions import ObjectDoesNotExist

from django.contrib.auth.models import User
from characters.models import Character
from forms import RegistrationForm, LoginForm, CharacterNameForm
from users.models import ExtendUser


def login_user(request):
	login_form = LoginForm(request.POST or None)
	
	if request.user.is_authenticated():
		return HttpResponseRedirect(request.POST.get('next') or reverse('index'))
	
	if request.POST and login_form.is_valid():
		user = login_form.login(request)
		if user:
			login(request, user)
			
			#add needed sessions
			if "order_by" not in request.session:
				request.session['order_by'] = 'id'
			if "order_by_last" not in request.session:
				request.session['order_by_last'] = False
			if "postdata" not in request.session:
				request.session['postdata'] = ""
			
			try:
				character = request.user.character_set.get(alive=True)
				return HttpResponseRedirect(request.POST.get('next') or reverse('index'))
			except ObjectDoesNotExist:
				return HttpResponseRedirect(reverse('create character'))
			
	return render(request, 'login.html', {'login_form': login_form, 'next': request.GET.get('next', '') })


# account views
# Register new user
#TODO: fix field errors in form
def register_user(request):
	# False till someone fills in and sends
	if request.method == "POST":
		form = RegistrationForm(request.POST)
		if form.is_valid():
			new_user = form.save(commit=False)
			new_user.save()
		
			#add extend user object
			new = ExtendUser(
				user=new_user,
			)
			new.save()
			
			return HttpResponseRedirect(reverse('login_user'))
	else:
		form = RegistrationForm()
	
	return render(request, 'register.html', {'form': form})
	
	
#Logout
def logout(request):
	auth.logout(request)
	return HttpResponseRedirect(reverse('login_user'))
	

def create_character(request):
	name_form = CharacterNameForm()
	
	if request.user.character_set.count() == 0:
		text = "Welcome to mercenaries, blabla its time to choose a name for your mercenary"
	else:
		text = "You died! If you want to start over and seek revenge, blabla, enter a new name and start again"
		
	
	if request.POST:
		name_form = CharacterNameForm(request.POST)
		
		if name_form.is_valid():
			name = name_form.cleaned_data['name']
			#create character
			Character.create(request.user, name)
			return HttpResponseRedirect(reverse('index'))
			
	return render(request, 'create_character.html', {"name_form": name_form, "text": text})

