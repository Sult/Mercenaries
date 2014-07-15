from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.context_processors import csrf
from django.core.exceptions import ObjectDoesNotExist, FieldError
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from mercs.decorators import still_alive
from mercs.helpers import sort_queryset_by_method, sort_queryset_by_field
from characters.forms import validate_contraband, check_for_contraband_input
from characters.forms import garage_actions, show_garage_regions, check_garage_actions, process_garage_actions
from characters.models import CharacterCar, CharacterGun
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
	max_booze = character.charactercontraband.get_maximum("booze")
	max_narcotics = character.charactercontraband.get_maximum("narcotics")
	
	
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
				return render(request, "inactive.html", {"result": narcotics_results.messages})
		
		if booze_check and narcotics_check:
			messages = booze_results.messages + narcotics_results.messages
		elif booze_check:
			messages = booze_results.messages
		elif narcotics_check:
			messages = narcotics_results.messages
		
		booze = character.charactercontraband.contraband_form("booze")
		narcotics = character.charactercontraband.contraband_form("narcotics")
				
		return render(request, 'contraband.html', {
													"booze": booze, "narcotics": narcotics, 
													"messages": messages, "max_booze": max_booze, "max_narcotics": max_narcotics})	
	
	return render(request, 'contraband.html', {"booze": booze, "narcotics": narcotics,
												"max_booze": max_booze, "max_narcotics": max_narcotics})	




#character cars overview
@login_required
@still_alive
def garage(request):
	character = request.user.character_set.get(alive=True)
	session = request.session
	
	#check if player is ready for job
	active = character.charactertimers.check_if_active()
	if active != True:
		return render(request, "inactive.html", {"result": active})
	
	message = ""
	if request.POST:
		if "item" not in request.POST and "confirm" not in request.POST:
			message = "Please select car(s)"
		
		elif session['postdata'] == "":
			message = check_garage_actions(request.POST, character)
			if not message[0]:
				message = message[1]
			else:
				#create dict of needed data for session
				postdata = {}
				postdata['action'] = request.POST['action']
				postdata['item'] = request.POST.getlist('item')
				session['postdata'] = postdata
				return render(request, "confirmation.html", {"message": message})
		else:
			if request.POST['confirm'] == "True":
				#execute postdata
				message = process_garage_actions(session['postdata'], character)
				session['postdata'] = ""
			
		
	# sorting
	if request.GET:
		order_by = request.GET.get('order_by', "id")
		region_name = request.GET.get('region', character.region.name)
		region = Region.objects.get(name=region_name)
		region_actions = show_garage_regions(region_name)
		
		
		if session['order_by'] == order_by:
			if session['order_by_last']:
				session['order_by_last'] = False
			else:
				session['order_by_last'] = True
		else:
			session['order_by'] = order_by
			if not session['order_by_last']:
				session['order_by_last'] = True
		
		if region == character.region:
			qs1 = CharacterCar.objects.filter(character=character, region=region).exclude(safe=None)
			qs2 = CharacterCar.objects.filter(character=character, safe=None)
			qs = qs1 | qs2
		else:
			safe = [False, True]
			qs = CharacterCar.objects.filter(character=character, region=region, safe__in=safe)
			
			
		
		if "health" in order_by:
			car_list = sort_queryset_by_method(qs, "hp_percent", session["order_by_last"])
		elif "price" in order_by:
			car_list = sort_queryset_by_method(qs, "price", session["order_by_last"])
		else:
			car_list = sort_queryset_by_field(qs, order_by, session["order_by_last"], relation="car")

	else:
		car_list = CharacterCar.objects.filter(character=character, region=character.region)
		region_name = character.region.name
		region_actions = show_garage_regions(region_name)
		
	#paginator
	paginator = Paginator(car_list, 25)
	page = request.GET.get("page")
	try:
		items = paginator.page(page)
	except PageNotAnInteger:
		items = paginator.page(1)
	except EmptyPage:
		items = paginator.page(paginator.num_pages)
	
	session['postdata'] = ""
	actions = garage_actions(character, character.region)

	return render(request, "garage.html", {"items": items, "region_name": region_name, 
											"actions": actions, "region_actions": region_actions,
											"message": message})




#contraband buy/sell view
@login_required
@still_alive
def gun_depot(request):
	pass




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

