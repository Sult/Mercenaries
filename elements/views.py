from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.context_processors import csrf
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required

from mercs.decorators import still_alive
from characters.models import CharacterTransport, CharacterHouse
from elements.models import Region, SinglePlayerJob, Transport, TravelMethod
from elements.forms import validate_transport, validate_travel_method, house_upgrade_form, housing_validation


#from operator import attrgetter, itemgetter
from collections import OrderedDict




@login_required
@still_alive
def short_job(request):
	character = request.user.character_set.get(alive=True)
	session = request.session
	timercheck = character.charactertimers.check_timer('short_job')
	
	if "short_job_list" not in request.session:
		session['short_job_list'] = SinglePlayerJob.get_job_list(character, SinglePlayerJob.SHORT)
	
	#check if player is ready for job
	if timercheck.check:
		part = "form"
		pagename = "short job"
	else:
		return render(request, "inactive.html", {"result": timercheck})
		
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
			return render(request, "singleplayerjob.html", {"results": results, "part": part, "pagename": pagename})
			
		except KeyError:
			return HttpResponseRedirect(reverse("short job"))
		
	#order job list
	job_list = sorted(session['short_job_list'],  key=session['short_job_list'].get, reverse=True)
	jobs = OrderedDict()
	
	for job in job_list:
		jobs[job] = session['short_job_list'][job]
	
	return render(request, "singleplayerjob.html", {"jobs": jobs, "part": part, "pagename": pagename})



@login_required
@still_alive
def medium_job(request):
	character = request.user.character_set.get(alive=True)
	session = request.session
	timercheck = character.charactertimers.check_timer('medium_job')
	
	
	if "medium_job_list" not in request.session:
		session['medium_job_list'] = SinglePlayerJob.get_job_list(character, SinglePlayerJob.MEDIUM)
	
	#check if player is ready for job
	if timercheck.check:
		part = "form"
		pagename = "medium job"
	else:
		return render(request, "inactive.html", {"result": timercheck})
		
	
	#if action is taken
	if request.POST:
		try:
			part = "result"
		
			# check if succeeds and give consequences
			job = request.POST["job"]
			chance = session['medium_job_list'][job]
			results = SinglePlayerJob.check_to_succeed(job, chance, character)
		
			#remove short_job_list and timer
			del session['medium_job_list']
			
			#update timer and xp
			character.perform_action("medium_job")
			
		except KeyError:
			return HttpResponseRedirect(reverse("medium job"))
		
		return render(request, "singleplayerjob.html", {"results": results, "part": part, "pagename": pagename})
	
	#order job list
	job_list = sorted(session['medium_job_list'],  key=session['medium_job_list'].get, reverse=True)
	jobs = OrderedDict()
	
	for job in job_list:
		jobs[job] = session['medium_job_list'][job]
	
	return render(request, "singleplayerjob.html", {"jobs": jobs, "part": part, "pagename": pagename})




#the market overview
@login_required
@still_alive
def market(request):
	character = request.user.character_set.get(alive=True)
	#check if player is ready for job
	active = character.charactertimers.check_if_active()
	if active != True:
		return render(request, "inactive.html", {"result": active})

	all_transports = CharacterTransport.objects.filter(character=character).order_by('region__name')
	all_houses = CharacterHouse.show_houses(character)
	
	return render(request, "market.html", {"all_transports": all_transports, "all_houses": all_houses})




# buy/sell transport and travelmethod
@login_required
@still_alive
def transport(request):
	character = request.user.character_set.get(alive=True)
	session = request.session
	
	#check if player is ready for job
	active = character.charactertimers.check_if_active()
	if active != True:
		return render(request, "inactive.html", {"result": active})
	
	#if character has no transport yet, give possible options to buy
	player_transport = CharacterTransport.objects.get(character=character, region=character.region)
	transports = {}
	if player_transport.transport == None:
		transports["buy"] = Transport.objects.all()
	else:
		transports["sell"] = player_transport.transport
	
	if request.POST:
		try:
			result = validate_transport(request.POST, character)
			if result == True:
				return HttpResponseRedirect(reverse("transport"))
			else:
				return render(request, "transport.html", {"transports": transports, "result": result})
		except KeyError:
			return HttpResponseRedirect(reverse("transport"))
	
	return render(request, "transport.html", {"transports": transports})


# buy sell new travel method
@login_required
@still_alive
def travel_method(request):
	character = request.user.character_set.get(alive=True)
	session = request.session
	
	#check if player is ready for job
	active = character.charactertimers.check_if_active()
	if active != True:
		return render(request, "inactive.html", {"result": active})
	
	remove = ["Hitchhike", character.charactertravel.transport.name]
	other_transports = TravelMethod.objects.exclude(name__in=remove)
	player_transport = character.charactertravel.transport
	
	
	if request.POST:
		try:
			result = validate_travel_method(request.POST, character)
			if result == True:
				return HttpResponseRedirect(reverse("travel method"))
			else:
				return render(request, "travel_method.html", {"other_transports": other_transports,
														"player_transport": player_transport, 
														"result": result})
		except KeyError:
			return HttpResponseRedirect(reverse("travel method"))
	
	return render(request, "travel_method.html", {"other_transports": other_transports,
													"player_transport": player_transport})




#buy housing
@login_required
#@still_alive
def housing(request):
	character = request.user.character_set.get(alive=True)
	
	#check if player is ready for job
	active = character.charactertimers.check_if_active()
	if active != True:
		return render(request, "inactive.html", {"result": active})
	
	try:
		temp = CharacterHouse.objects.get(character=character, region=character.region)
		house = temp.view_house()
		storage = temp.total_storage()	
	except ObjectDoesNotExist:
		house = None
		storage = {}
	
	upgrades = house_upgrade_form(character)
	
	
	if request.POST:
		result = housing_validation(request.POST, character)
		if result == True:
			return HttpResponseRedirect(reverse("housing"))
		else:
			return render(request, "housing.html", {"house": house, "upgrades": upgrades, "storage": storage, "result": result})
	
	return render(request, "housing.html", {"house": house, "upgrades": upgrades, "storage": storage})
	


