from django import forms
from django.utils.timezone import utc
from django.core.exceptions import ObjectDoesNotExist

from elements.models import Region, RegionPrices, convert_damn
from characters.models import CharacterContraband, CharacterHouse, CharacterCar

from collections import namedtuple
from datetime import datetime




class TravelForm(forms.Form):
	""" travel form, own location excluded """
	
	travel = forms.ModelChoiceField(empty_label=None, 
									queryset=Region.objects.all(),
									widget=forms.RadioSelect())
	
	
	def __init__(self, *args, **kwargs):
		exclude_args = kwargs.pop('exclude', {})
		super(TravelForm, self).__init__(*args, **kwargs)
		self.fields['travel'].queryset = Region.objects.exclude(**exclude_args)




def check_for_contraband_input(postdata, smuggle):
	contraband_items = CharacterContraband.get_booze_or_narcotics(smuggle)
	
	counter = 0
	for item in contraband_items:
		try:
			int(postdata[item])
			counter += 1
		except ValueError:
			pass
	
	if counter > 0:
		return True
	else:
		return False



def validate_contraband(postdata, character, smuggle):
	# set returning data
	Results = namedtuple("Results", "valid messages")
	messages = []

	#check if the buy/sell values are given so code doesnt crash on faulty input
	buy = True
	try:
		if postdata[smuggle] == "sell":
			buy = False
	except KeyError:
		messages.append("Please select buy or sell")
		return Results(valid=False, messages=messages)
	
	
	#get contraband item list (booze or narcotics)
	contraband = character.charactercontraband
	contraband_items = contraband.get_booze_or_narcotics(smuggle)
	
	#to hold the item data, buy = False when selling
	Item = namedtuple("Item", "name amount price buy")
			
	
	#current regional prices
	prices = character.region.regionprices
	#convert postdata to workable list
	form_items = []
	for item in contraband_items:
		try:
			amount = int(postdata[item])
			owned_units = getattr(contraband.contraband, item)
			price = getattr(prices, item)
			form_items.append(Item(name=item, amount=amount, price=price, buy=buy))		
		except ValueError:
			pass

	
	total_damn = 0
	total_amount = 0
	for item in form_items:
		total_damn += item.amount * item.price
		total_amount += item.amount
	
	
	# check if player has enough room to buy
	max_contraband = contraband.get_maximum(smuggle)
	current_contraband = contraband.get_current(smuggle)
	
	if buy:
		if current_contraband + total_amount > max_contraband:
			message = "You can only buy %s items of %s." % (max_contraband - current_contraband, smuggle)
			messages.append(message)
			return Results(valid=False, messages=messages)
	
	
	#if selling see if player has enough of each to sell
	else:
		counter = 0
		for item in form_items:
			you_got = getattr(contraband.contraband, item.name)
			if you_got < item.amount:
				message = "You don't have so many %s to sell." % item.name
				messages.append(message)
				counter += 1
		
		if counter > 0:
			return Results(valid=False, messages=messages)
	
	
	# Check if player has enough money if he tries to buy
	if buy:
		if not character.check_damn(total_damn):
			message = "You do not have enough money to buy your %s." % smuggle
			messages.append(message)
			return Results(valid=False, messages=messages)
	
	
	#see if player succeeds in smuggling
	check = character.try_to_smuggle(smuggle)
	
	#if still no returns, add/remove items and add/remove damn
	if check == True:
		if buy:
			for item in form_items:
				current = getattr(contraband.contraband, item.name)
				setattr(contraband.contraband, item.name, current + item.amount)
		
			character.update_damn(-total_damn)
		
			#see if character receives xp for smuggling (only on buying)
			now = datetime.utcnow().replace(tzinfo=utc)
			timer = getattr(character.charactertimers, smuggle)
	
			if timer < now:
				#add xp and set timers
				character.perform_action(smuggle, times=total_amount)
	
		else:
			for item in form_items:
				current = getattr(contraband.contraband, item.name)
				setattr(contraband.contraband, item.name, current - item.amount)
			
			character.update_damn(total_damn)
	
		character.save()
		contraband.save()
		contraband.contraband.save()
		return Results(valid=True, messages=messages)
	
	else:
		return Results(valid=None, messages=check)
	


def show_garage_regions(region_name):
	regions = Region.objects.exclude(name=region_name)
	actions = []
	for region in regions:
		actions.append([region.name, region.name])
	return actions

	

def garage_actions(character, region):
	actions = [
		["repair", "repair car(s)"],
		["sell", "sell car(s)"],
	]
	
	try:
		amount_house = CharacterHouse.objects.get(character=character, region=region).garage.cars
		if amount_house > 0:
			stored = CharacterCar.objects.filter(character=character, safe=True, region=region).count()
			if stored > 0:
				actions.append(["house remove", "Remove from safehouse"])
			if amount_house > stored:
				actions.append(["house add", "Park in safehouse"])
	except ObjectDoesNotExist:
		pass
	
	#add options for loading on helicopter
	amount_travel = character.charactertravel.transport.cars
	
	if amount_travel > 0:
		stored = CharacterCar.objects.filter(character=character, safe=None).count()
		if stored > 0:
			actions.append(["travel remove", "Unload from helicopter"])
		
		if amount_travel > stored:
			actions.append(["travel add", "Load on helicopter"])
	
	return actions
	
	
	

# generate confirmation message 
def check_garage_actions(postdata, character):
	#return confirmation message with repair costs
	try:
		if postdata['action'] == "repair":
			repair_cost = CharacterCar.total_from_function(postdata.getlist('item'), "repair_cost", character)
			
			# if total_form_function encountered ids that dont exist or belong to character, return false
			# also return false when total repair price is 0
			if isinstance(repair_cost, bool):
				if len(postdata.getlist('item')) > 1:
					return False, "You do not own these cars!"
				else:
					return False, "You do not own this car!"
			elif repair_cost == 0:
				if len(postdata.getlist('item')) > 1:
					return False, "These cars are not damaged."
				else:
					return False, "This car is not damaged."
				
				return False, ""
		
			message = ""
			if len(postdata.getlist('item')) > 1:
				message = "Are you sure you want to repair these cars for a total cost of %s?" % convert_damn(repair_cost)
			else:
				message = "Are you sure you want to repair this car for a cost of %s?" % convert_damn(repair_cost)
		
			return message
	
		#return confirmation message with sellprice
		elif postdata['action'] == "sell":
			total_price = CharacterCar.total_from_function(postdata.getlist('item'), "price", character)
			# if total_form_function encountered ids that dont exist or belong to character, return false
			if isinstance(total_price, bool):
				if len(postdata.getlist('item')) > 1:
					return False, "You do not own these cars!"
				else:
					return False, "You do not own this car!"
			
			message = ""
			if len(postdata.getlist('item')) > 1:
				message = "Are you sure you want to sell these cars for a total price of %s?" % convert_damn(total_price)
			else:
				message = "Are you sure you want to sell this car for a price of %s?" % convert_damn(total_price)
		
			return message
		
		#put car(s) in a helicopter
		elif postdata['action'] == "travel add":
			count = len(postdata.getlist('item'))
			
			# see if user does not select to many cars
			max_room = character.charactertravel.car_room_left()
			if count > max_room:
				if max_room > 1:
					return False, "You only have room for %d more cars." % max_room
				else:
					return False, "You only have room for one more car."
			
			#ask confirmation
			else:
				if count > 1:
					return "Are you sure you want to load these cars into your helicopter?"
				else:
					return "Are you sure you want to load this car into your helicopter?"
		
		#remove cars from helicopter
		elif postdata['action'] == "travel remove":
			car_ids = postdata.getlist('item')
			count = len(car_ids)
			
			#see if cars are not in helicopter
			counter = 0
			for pk in car_ids:
				car = CharacterCar.objects.get(id=pk, character=character)
				if car.safe != None:
					counter += 1
				
			if counter > 1:
				return False, "Some of these cars are not in your helicopter!"
			elif counter == 1:
				return False, "One of these cars is not in your helicopter!"
			else:
				if count > 1:
					return "Are you sure you want to unload these cars from your helicopter?"
				else:
					return "Are you sure you want to unload this car from your helicopter?"
		
		#put car(s) in a safehouse
		elif postdata['action'] == "house add":
			count = len(postdata.getlist('item'))
			
			# see if user does not select to many cars
			max_room = CharacterHouse.objects.get(character=character, region=character.region).car_room_left()
			if count > max_room:
				if max_room > 1:
					return False, "You only have room for %d more cars." % max_room
				else:
					return False, "You only have room for one more car."
			
			#ask confirmation
			else:
				if count > 1:
					return "Are you sure you want to park these cars into your safehouse?"
				else:
					return "Are you sure you want to park this car into your safehouse?"
		
		#remove cars from helicopter
		elif postdata['action'] == "house remove":
			car_ids = postdata.getlist('item')
			count = len(car_ids)
			
			#see if cars are not in helicopter
			counter = 0
			for pk in car_ids:
				car = CharacterCar.objects.get(id=pk, character=character)
				if car.safe != True:
					counter += 1
				
			if counter > 1:
				return False, "Some of these cars are not parked in your safehouse!"
			elif counter == 1:
				return False, "One of these cars is not parked in your safehouse!"
			else:
				if count > 1:
					return "Are you sure you want to remove these cars from your safehouse?"
				else:
					return "Are you sure you want to remove this car from your safehouse?"
		
		
	#	
	except KeyError:
		return False, "You did not select an action"
	


# after confirming, process the data and return results
def process_garage_actions(postdata, character):
	# repair cars
	if postdata['action'] == "repair":
		car_ids = postdata['item']
		repair_cost = CharacterCar.total_from_function(car_ids, "repair_cost", character)
		# if player has enough damn, repair all cars and pay costs
		if character.check_damn(repair_cost):
			character.update_damn(-repair_cost)
			
			for pk in car_ids:
				CharacterCar.objects.get(id=pk).repair_car()
			
			if len(car_ids) > 1:	
				return "You repaired %d cars for a total of %s." % (len(car_ids), convert_damn(repair_cost))
			else:
				return "You repaired your car for a %s." % convert_damn(repair_cost)
		
		else:
			return "You do not have enough damn."
	
	# sell cars
	elif postdata['action'] == "sell":
		car_ids = postdata['item']
		total_price = CharacterCar.total_from_function(car_ids, "price", character)
		character.update_damn(total_price)
		
		for pk in car_ids:
			CharacterCar.objects.get(id=pk).delete()
		
		if len(car_ids) > 1:
			return "You sold %d cars for a total of %s" % (len(car_ids), convert_damn(total_price))
		else:
			return "You sold this car for %s" % convert_damn(total_price)
	
	
	# put car into helicopter
	elif postdata['action'] == "travel add":
		car_ids = postdata['item']
		travel = character.charactertravel
		for pk in car_ids:
			car = CharacterCar.objects.get(id=pk)
			car.safe = None
			car.save()
			travel.add_car(car)
			
		if len(car_ids) > 1:
			return "The cars are now safely loaded inside your helicopter."
		else:
			return "The car is now safely loaded inside your helicopter."
			
	# Remove cars from helicopter
	elif postdata['action'] == "travel remove":
		car_ids = postdata['item']
		travel = character.charactertravel
		
		for pk in car_ids:
			car = CharacterCar.objects.get(id=pk)
			car.safe = False
			car.save()
			travel.remove_car(car)
		
		if len(car_ids) > 1:
			return "The cars are unloaded from your helicopter."
		else:
			return "The car is unloaded from your helicopter."


	# put car into helicopter
	elif postdata['action'] == "house add":
		car_ids = postdata['item']
		house = CharacterHouse.objects.get(character=character, region=character.region)
		for pk in car_ids:
			car = CharacterCar.objects.get(id=pk)
			car.safe = True
			car.save()
			house.add_car(car)
			
		if len(car_ids) > 1:
			return "The cars are now safely parked inside your safehouse."
		else:
			return "The car is now safely parked inside your safehouse."

	# Remove cars from helicopter
	elif postdata['action'] == "house remove":
		car_ids = postdata['item']
		house = CharacterHouse.objects.get(character=character, region=character.region)
		
		for pk in car_ids:
			car = CharacterCar.objects.get(id=pk)
			car.safe = False
			car.save()
			house.remove_car(car)
		
		if len(car_ids) > 1:
			return "The cars are removed from your safehouse."
		else:
			return "The car is removed from your safehouse."









