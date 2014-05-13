from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.core.context_processors import csrf
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required

from characters.models import CharacterTransport
from elements.models import Region, SinglePlayerJob

#from operator import attrgetter, itemgetter
from collections import OrderedDict


@login_required
def short_job(request):
	character = request.user.character
	session = request.session
	timercheck = character.charactertimers.check_timer('short_job')
	timer = timercheck.timer
	
	if "short_job_list" not in request.session:
		session['short_job_list'] = SinglePlayerJob.get_job_list(character, SinglePlayerJob.SHORT)
	
	#check if player is ready for job
	if timercheck.check:
		part = "form"
	else:
		part = "timer"
		
	#if action is taken
	if request.POST:
		try:
			part = "result"
		
			# check if succeeds and give consequences
			job = request.POST["job"]
			chance = session['short_job_list'][job]
			results = SinglePlayerJob.check_to_succeed(job, chance, character)
		
			#remove short_job_list and timer
			del session['short_job_list']
			
			#update timer and xp
			character.perform_action("short_job")
			return render(request, "singleplayerjob.html", {"results": results, "part": part})
			
		except KeyError:
			return HttpResponseRedirect(reverse("short job"))
		
		
	
	#order job list
	job_list = sorted(session['short_job_list'],  key=session['short_job_list'].get, reverse=True)
	jobs = OrderedDict()
	
	for job in job_list:
		jobs[job] = session['short_job_list'][job]
	
	return render(request, "singleplayerjob.html", {"jobs": jobs, "timer": timer, "part": part})



def medium_job(request):
	character = request.user.character
	session = request.session
	timercheck = character.charactertimers.check_timer('medium_job')
	timer = timercheck.timer
	
	if "medium_job_list" not in request.session:
		session['medium_job_list'] = SinglePlayerJob.get_job_list(character, SinglePlayerJob.MEDIUM)
	
	#check if player is ready for job
	if timercheck.check:
		part = "form"
	else:
		part = "timer"
		
	
	#if action is taken
	if request.POST:
		try:
			part = "result"
		
			# check if succeeds and give consequences
			job = request.POST["job"]
			chance = session['medium_job_list'][job]
			
			#make different loot results
			results = SinglePlayerJob.check_to_succeed(job, chance, character)
		
			#remove short_job_list and timer
			del session['medium_job_list']
			
			#update timer and xp
			character.perform_action("medium_job")
			
		except KeyError:
			return HttpResponseRedirect(reverse("medium job"))
		
		return render(request, "singleplayerjob.html", {"results": results, "part": part})
	
	
	#order job list
	job_list = sorted(session['medium_job_list'],  key=session['medium_job_list'].get, reverse=True)
	jobs = OrderedDict()
	
	for job in job_list:
		jobs[job] = session['medium_job_list'][job]
	
	return render(request, "singleplayerjob.html", {"jobs": jobs, "timer": timer, "part": part})




#the market overview
@login_required
def market(request):
	#not sure this overview is needed
	transports = CharacterTransport.transport_overview(request.user.character)
	
	
	
	return render(request, "market.html", {"transports": transports})
	

