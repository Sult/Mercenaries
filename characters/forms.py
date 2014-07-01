from django import forms
from django.utils.timezone import utc

from elements.models import Region, RegionPrices
from characters.models import CharacterContraband
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
			owned_units = getattr(contraband, item)
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
			you_got = getattr(contraband, item.name)
			if you_got < item.amount:
				message = "You don't have so many %s to sell." % item.name
				messages.append(message)
				counter += 1
		
		if counter > 0:
			return Results(valid=False, messages=messages)
	
	
	# Check if player has enough money if he tries to buy
	if buy:
		if character.damn < total_damn:
			message = "You do not have enough money to buy your %s." % smuggle
			messages.append(message)
			return Results(valid=False, messages=messages)
	
	
	#see if player succeeds in smuggling
	check = character.try_to_smuggle(smuggle)
	
	#if still no returns, add/remove items and add/remove damn
	if check == True:
		if buy:
			for item in form_items:
				current = getattr(contraband, item.name)
				setattr(contraband, item.name, current + item.amount)
		
			character.damn -= total_damn
		
			#see if character receives xp for smuggling (only on buying)
			now = datetime.utcnow().replace(tzinfo=utc)
			timer = getattr(character.charactertimers, smuggle)
	
			if timer < now:
				#add xp and set timers
				character.perform_action(smuggle, times=total_amount)
	
		else:
			for item in form_items:
				current = getattr(contraband, item.name)
				setattr(contraband, item.name, current - item.amount)
			
			character.damn += total_damn
	
		character.save()
		contraband.save()
		return Results(valid=True, messages=messages)
	
	else:
		return Results(valid=None, messages=check)
	
	
	
	
	
	
	
	
	
