from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.core.context_processors import csrf
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required


@login_required
def index(request):
	
	return render(request, 'index.html') 



@login_required
def character(request):
	character = request.user.character
	basic = character.basic_information()
	possessions = character.possessions()
	status = character.status()
	timers = character.charactertimers.timers()
	work = character.work_experience()
	return render(request, 'character.html', {"basic": basic,
												"possessions": possessions,
												"status": status,
												"timers": timers,
												"work": work}) 

	


def medium_job(request):
	pass


def long_job(request):
	pass
	

def contraband(request):
	pass
	


def group_crime(request):
	pass



def travel(request):
	pass


def blood(request):
	pass


def race(request):
	pass


def kill(request):
	pass


def bullet_deal(request):
	pass

