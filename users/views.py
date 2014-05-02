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
from forms import RegistrationForm, LoginForm



def login_user(request):
	login_form = LoginForm(request.POST or None)
	
	if request.user.is_authenticated():
		return HttpResponseRedirect(request.POST.get('next') or reverse('index'))
	
	if request.POST and login_form.is_valid():
		user = login_form.login(request)
		if user:
			login(request, user)
			return HttpResponseRedirect(request.POST.get('next') or reverse('index'))
			
	return render(request, 'login.html', {'login_form': login_form, 'next': request.GET.get('next', '') })


# account views
# Register new user
def register_user(request):
	# False till someone fills in and sends
	if request.method == "POST":
		form = RegistrationForm(request.POST)
		if form.is_valid():
			new_user = form.save(commit=False)
			new_user.save()

			#Create Character
			Character.create(new_user)
			
			return HttpResponseRedirect(reverse('index'))
	else:
		form = RegistrationForm()
	
	return render(request, 'register.html', {'form': form})
	
	
#Logout
def logout(request):
	auth.logout(request)
	return HttpResponseRedirect(reverse('login_user'))
	



