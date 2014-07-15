from django import forms
from django.core.exceptions import ObjectDoesNotExist

from elements.models import Transport, TravelMethod, Housing
from characters.models import CharacterTransport, CharacterHouse, Contraband

from collections import namedtuple



def validate_transport(postdata, character):
	buy = True
	
	if 'sell' in postdata:
		buy = False
	
	character_transport = CharacterTransport.objects.get(character=character, region=character.region)
	
	# check if character has enough damn if so, add item
	if buy:
		transport = Transport.objects.get(name=postdata['buy'])
		if not character.check_damn(transport.price):
			return "You don't have enough damns to give!"
		else:
			character.update_damn(-transport.price)
			character_transport.transport = transport
			character_transport.save()
			return True
	
	#if selling, set to default and add damn
	else:
		character.update_damn(+ int(character_transport.transport.price / 2))
		character_transport.transport = None
		character_transport.save()
		return True
		
	

# purchasing a new travel method 
def validate_travel_method(postdata, character):
	buy = True
	
	if 'sell' in postdata:
		buy = False
	
	# if buying new travel method
	if buy:
		travel_method = TravelMethod.objects.get(name=postdata['buy'])
		if not character.check_damn(travel_method.price):
			return "You don't have enough damns to give!"
		else:
			character.update_damn(- travel_method.price)
			character.charactertravel.transport = travel_method
			character.charactertravel.save()
			return True
	
	#when selling a travel method
	else:
		if character.charactertravel.car1 == None and character.charactertravel.car2 == None:
			travel_method = TravelMethod.objects.get(name="Hitchhike")
			character.update_damn(+ int(character.charactertravel.transport.price / 2))
			character.charactertravel.transport = travel_method
			character.save()
			character.charactertravel.save()
			return True
		else:
			return "You have to unload your cars first."
		



# create data for housing shop form
def	house_upgrade_form(character):
	upgrades = []
	
	try:
		house = CharacterHouse.objects.get(region=character.region, character=character)
	except ObjectDoesNotExist:
		upgrades.append(Housing.objects.get(name="Building Lot"))
		return upgrades
	
	
	#get house upgrade
	if house.house.rank < 4:
		upgrades.append(Housing.objects.get(category=Housing.HOUSE, rank=house.house.rank + 1))
	
	sub_spaces = ['basement', 'garage', 'garden']
	
	#add possible sub upgrades
	for sub in sub_spaces:
		part = getattr(house, sub)
		
		# if house has no sub yet
		if part != None:
			
			#if house rank is high enough for upgrade
			if part.rank < house.house.rank:
				#make sure player can only upgrade bunker once
				if sub == "basement":
					if part.rank == 3:
						bunker = Housing.objects.get(name="Bunker")
						try:
							CharacterHouse.objects.get(character=character, basement=bunker)
						except ObjectDoesNotExist:
							upgrades.append(bunker)
			
					else:
						upgrades.append(Housing.objects.get(category=sub, rank=part.rank + 1))
				else:
					upgrades.append(Housing.objects.get(category=sub, rank=part.rank + 1))
		
		#add first level upgrade if house rank is 1 or higher
		else:
			if house.house.rank > 0:
				upgrades.append(Housing.objects.get(category=sub, rank=1))
			
	return upgrades	
	
	
	
	
	
#validate postdata and create/upgrade housing
def housing_validation(postdata, character):
	building_lot = Housing.objects.get(name="Building Lot")
	#create CharacterHouse object
	building = Housing.objects.get(id=int(postdata['buy']))
	
	if not character.check_damn(building.price):
		return "You do not have enough damn to build this building lot."
	
	#create new house
	if building_lot.id == building.id:
		character.update_damn(-building_lot.price)
		
		new_house = CharacterHouse(
			character=character,
			contraband=Contraband.create(),
			region=character.region,
			house=building_lot,
		)
		new_house.save()
		return True
	
	else:
		character.update_damn(-building.price)
		house = CharacterHouse.objects.get(character=character, region=character.region)
		setattr(house, building.category, building)
		house.save()
		return True
		
		
		
		
		
		
		
		
		
		
		
		
		
		
