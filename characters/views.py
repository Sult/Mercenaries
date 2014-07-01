from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.context_processors import csrf
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required

from mercs.decorators import still_alive
from characters.forms import validate_contraband, check_for_contraband_input
from elements.models import Region

@login_required
@still_alive
def index(request):
	
	return render(request, 'index.html') 



@login_required
@still_alive
def character(request):
	character = request.user.character_set.get(alive=True)
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


@login_required
@still_alive
def travel(request):
	character = request.user.character_set.get(alive=True)
	timercheck = character.charactertimers.check_timer('travel')
	
	#check if player is ready to travel
	if timercheck.check:
		part = "form"
	else:
		return render(request, "inactive.html", {"result": timercheck})
	
	travel_to = character.travel_stats()
	
	if request.POST:
		part = "result"
		result = character.travel(request.POST['travel_to'])
		return render(request, "travel.html", {"part": part, "result": result})
		
	return render(request, "travel.html", {"travel_to": travel_to,
											"part": part})

	

#contraband buy/sell view
@login_required
@still_alive
def contraband(request):
	character = request.user.character_set.get(alive=True)
	session = request.session
	timercheck = character.charactertimers.check_timer('booze', contraband=True)
	
	#check if player is ready to travel
	if timercheck.check == False:
		return render(request, "inactive.html", {"result": timercheck})

	booze = character.charactercontraband.contraband_form("booze")
	narcotics = character.charactercontraband.contraband_form("narcotics")
	
	if request.POST:
		#check if there is booze data and handle results
		booze_check = check_for_contraband_input(request.POST, "booze")
		
		if booze_check:
			booze_results = validate_contraband(request.POST, character, "booze")
			if booze_results.valid == None:
				return render(request, "inactive.html", {"result": booze_results.messages})
		
		#repeat for narcotics
		narcotics_check = check_for_contraband_input(request.POST, "narcotics")
		
		if narcotics_check:
			narcotics_results = validate_contraband(request.POST, character, "narcotics")
			if narcotics_results.valid == None:
				return render(request, "inactive.html", {"result": booze_results.messages})
		
		if booze_check and narcotics_check:
			messages = booze_results.messages + narcotics_results.messages
		elif booze_check:
			messages = booze_results.messages
		elif narcotics_check:
			messages = narcotics_results.messages
		
		booze = character.charactercontraband.contraband_form("booze")
		narcotics = character.charactercontraband.contraband_form("narcotics")
				
		return render(request, 'contraband.html', {"booze": booze, "narcotics": narcotics, "messages": messages})	
	
	return render(request, 'contraband.html', {"booze": booze, "narcotics": narcotics})	







def long_job(request):
	pass
	


	


def group_crime(request):
	pass





def blood(request):
	pass


def race(request):
	pass


def kill(request):
	pass


def bullet_deal(request):
	pass

