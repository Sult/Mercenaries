#TODO: Make cache vars for the job/car/gun lists etc
from django.db import models
from django.core.exceptions import ObjectDoesNotExist

from characters.models import CharacterCar, CharacterArmor, CharacterGun, Character
from mail.models import Mail

from random import randint, choice, shuffle
from collections import namedtuple, OrderedDict
from datetime import datetime, timedelta
from math import sqrt


#convert damn to currency
def convert_damn(damn):
	return '{:,}'.format(damn) + " Dmn"


#File upload name maker
def get_upload_file_name(instance, filename):
	return "uploaded_portraits/%s_%s" % (str(time()).replace('.','_'), filename)


#get result for min/max/random equation
def get_min_max_result(minimum, maximum, chance, rank):
	# Example: minimum = 15, maximum = 50, chance = 40, character.rank.rank = 5
	# max_ranks = 12
	# base = (50 - 15)/ 12 * 5 = 14.58
	# char_base = 14.58 / 100 * (100 - 40) = 8.75
	# rand_base // 14.58 - 8.75 = 5.83 // random between 0 and 5 (integer) = 3
	# total = integer of 15 + 14.58 + 3 = 32
	
	max_ranks = Rank.objects.all().count() - 2									#-4 for the double ranks
	base = (maximum - minimum + 0.0) / max_ranks * rank			
	char_base = base / 100 * (100 - chance)
	rand_base = randint(0, int(base - char_base))
	total = rand_base + char_base + minimum
	return int(total)
	

# convert timedelta to readable time
def convert_timedelta(duration):
	days, seconds = duration.days, duration.seconds
	hours = days * 24 + seconds // 3600
	minutes = (seconds % 3600) // 60
	seconds = (seconds % 60)
	
	string = ""
	if hours > 0:
		string += "{}H".format(hours)
	if minutes > 0:
		string += " {}M".format(minutes)
	if seconds > 0:
		string += " {}S".format(seconds)
	
	return string



#get a random car from raritylist
def random_object_by_model(modelname, **kwargs):
	try:
		model = models.get_model("elements", modelname)
		all_objects = model.objects.filter(**kwargs)
		pick_list = []
		for obj in all_objects:
			pick_list.extend([obj] * obj.rarity)
		
		return choice(pick_list)
	except AttributeError:
		print "Model does not exist or has no rarity"


class Result(namedtuple("Result", "check category flavor")):
	def __new__(cls, check=True, category="Error", flavor="Error, please report to admin"):
		return super(Result, cls).__new__(cls, check, category, flavor)


def convert_timer(timer, **kwargs):
	if "seconds" in kwargs:
		timer /= 60
		
	hours = timer // 60
	minutes = timer % 60
	
	if hours == 0 and minutes == 0:
		return "Instant" 
	if hours == 0:
		return "%d minutes" % minutes 
	
	result = ""
	extra = "s" if hours > 1 else ""
	
	if hours > 0 and minutes == 0:
		result += "%d hour%s" % (hours, extra)
	elif hours > 0:
		result += "%d hour%s and " % (hours, extra)
		
	if minutes > 0:
		result += "%d minutes" % minutes
	
	return result
		




class Rank(models.Model):
	""" Ranks with their stats """
	
	name = models.CharField(max_length=31, unique=True)
	special = models.BooleanField()
	rank = models.IntegerField()
	min_xp = models.IntegerField()
	max_xp = models.IntegerField()
	hitpoints = models.IntegerField()
	booze = models.IntegerField()
	narcotics = models.IntegerField()
	
	def __unicode__(self):
		return self.name

	
	
class TravelMethod(models.Model):
	""" all plane types you can buy in market """
	
	name = models.CharField(max_length=63, unique=True)
	travel_timer = models.IntegerField()								# in seconds
	price = models.IntegerField()
	description = models.TextField()
	travel_modifier = models.IntegerField()
	
	#cargo
	guns = models.IntegerField()										
	cars = models.IntegerField()
	booze = models.IntegerField()										# extra on top of rank
	narcotics = models.IntegerField()										# extra on top of rank
	
	image = models.FileField(upload_to=get_upload_file_name, null=True)
	
	
	def __unicode__(self):
		return self.name
	
	
	# show price in templates
	def show_price(self):
		return convert_damn(self.price)
		
	# show sell price in templates
	def show_sell_price(self):
		return convert_damn(int(self.price / 2))
		
	#show travel timer in templates
	def show_travel_timer(self):
		return convert_timer(self.travel_timer, seconds=True)
	

class Transport(models.Model):
	""" transport possible on location itself (enhances kill/survive attempts)"""
	
	name = models.CharField(max_length=63)
	attack = models.IntegerField()							# percent on total attack
	defense = models.IntegerField()							# percent vs total attack
	price = models.IntegerField()
	equip = models.IntegerField()							#time in minutes
	
	image = models.FileField(upload_to=get_upload_file_name, null=True)
	
	def __unicode__(self):
		return self.name
	
	def buy_price(self):
		return convert_damn(self.price)
		
	def sell_price(self):
		return convert_damn(int(self.price / 2))
	
	def equip_timer(self):
		return convert_timer(self.equip)
	


class Armor(models.Model):
	""" armor objects that players can equip """
	
	TYPE_I = "Type I"
	TYPE_IIA = "Type IIA"
	TYPE_II = "Type II"
	TYPE_IIIA = "Type IIIA"
	TYPE_III = "Type III"
	TYPE_IV = "Type IV"
	CATEGORIES = (
		(TYPE_I, "Type I"),
		(TYPE_IIA, "Type IIA"),
		(TYPE_II, "Type II"),
		(TYPE_IIIA, "Type IIIA"),
		(TYPE_III, "Type III"),
		(TYPE_IV, "Type IV"),

	)
	
	BAD = "Bad"
	NORMAL = "Normal"
	GOOD = "Good"
	QUALITY = (
		(BAD, "Bad"),
		(NORMAL, "Normal"),
		(GOOD, "Good"),
	)
	
	
	name = models.CharField(max_length=63)
	rarity = models.IntegerField()
	category = models.CharField(max_length=15, choices=CATEGORIES)
	quality	= models.CharField(max_length=7, choices=QUALITY)
	defense = models.IntegerField()
	equip = models.IntegerField()										#time in minutes
	price = models.IntegerField()
	
	image = models.FileField(upload_to=get_upload_file_name, null=True)
	
	def __unicode__(self):
		return self.name
	



class Gun(models.Model):
	""" all different guns available in game """
	
	PISTOL = "Pistol"
	MACHINE_PISTOL = "Machine Pistol"
	SHOTGUN = "Shotgun"
	ASSAULT_RIFLE = "Assault Rifle"
	SNIPER_RIFLE = "Sniper Rifle"
	CATEGORIES = (
		(PISTOL, "Pistol"),
		(MACHINE_PISTOL, "Machine Pistol"),
		(SHOTGUN, "Shotgun"),
		(ASSAULT_RIFLE, "Assault Rifle"),
		(SNIPER_RIFLE, "Sniper Rifle"),
	)
	
	name = models.CharField(max_length=63)
	rarity = models.IntegerField(max_length=31)
	category = models.CharField(max_length=31, choices=CATEGORIES)
	accuracy = models.FloatField()
	magazine = models.IntegerField()
	damage = models.IntegerField()
	price = models.IntegerField()
	
	image = models.FileField(upload_to=get_upload_file_name, null=True)	
	
	def __unicode__(self):
		return self.name



class Car(models.Model):
	""" all different cars available in game """
	
	SPORTSCAR = "Sports Car"
	TRUCK = "Truck"
	PICKUP = "Pickup"
	CAR = "Car"
	JEEP = "Jeep"
	CATEGORIES = (
		(SPORTSCAR, "Sports Car"),
		(TRUCK, "Truck"),
		(PICKUP, "Pickup"),
		(CAR, "Car"),
		(JEEP, "Jeep"),
	)
	
	name = models.CharField(max_length=31)
	category = models.CharField(max_length=15, choices=CATEGORIES)
	rarity = models.IntegerField()
	speed = models.IntegerField()
	seats = models.IntegerField()
	max_seats = models.IntegerField()
	max_hitpoints = models.IntegerField()
	price = models.IntegerField()
	
	
	image = models.FileField(upload_to=get_upload_file_name, null=True)
	
	def __unicode__(self):
		return self.name


	def random_hp(self):
		return randint(1, self.max_hitpoints)
		
		
	
	
class Region(models.Model):
	""" type of booze and their base price """
	
	name = models.CharField(max_length=31, unique=True)
	alliance_slots = models.IntegerField()					#Maximum amounts of alliances in this region
	
	#coordinates
	x = models.IntegerField()
	y = models.IntegerField()
	
	#base contraband prices
	beer = models.FloatField()
	cider = models.FloatField()
	cognaq = models.FloatField()
	rum = models.FloatField()
	vodka = models.FloatField()
	whiskey = models.FloatField()
	wine = models.FloatField()
	
	cocaine = models.FloatField()
	tabacco = models.FloatField()
	morphine = models.FloatField()
	glue = models.FloatField()
	amfetamines = models.FloatField()
	heroin = models.FloatField()
	cannabis = models.FloatField()
	
	def __unicode__(self):
		return self.name
	
	
	#get travel cost
	def get_travel_cost(self, destination, character):
		x = abs(self.x - destination.x)
		y = abs(self.y - destination.y)
		distance = sqrt(x**2 + y**2)
		
		cost = int(distance * character.charactertravel.transport.travel_modifier)
		return cost

	

class RegionPrices(models.Model):
	""" Holds current booze/narcs prices per region"""
	
	region = models.OneToOneField(Region)
	
	beer = models.IntegerField()
	cider = models.IntegerField()
	cognaq = models.IntegerField()
	rum = models.IntegerField()
	vodka = models.IntegerField()
	whiskey = models.IntegerField()
	wine = models.IntegerField()
	
	cocaine = models.IntegerField()
	tabacco = models.IntegerField()
	morphine = models.IntegerField()
	glue = models.IntegerField()
	amfetamines = models.IntegerField()
	heroin = models.IntegerField()
	cannabis = models.IntegerField()
	
	def __unicode__(self):
		return "%s prices" % region.name
		
	
	#def region_contraband_prices(self, contraband):
		#items = []
		
		#if contraband == "booze":
			#items = ['beer', 'cider', 'cognaq', 'rum', 'vodka', 'whiskey', 'wine']
		#elif contraband == "narcotics":
			#items = ['cocaine', 'tabacco', 'morphine', 'glue', 'amfetamines', 'heroin', 'cannabis']
		#else:
			#print "bad input for contraband, use 'booze' or 'narcotics'"
			#return
		
		#booze_dict = {}
		
		#for item in items:
			#booze_dict[item] = getattr(self, item)
		
		#return booze_dict
		
	
	


class GameBaseValues(models.Model):
	""" Base numbers that help tweaking the mechanics of the game """
	
	#All game timers (in seconds)
	##Normal actions
	travel = models.IntegerField()
	blood_buy = models.IntegerField()
	car_race = models.IntegerField()
	kill_attempt = models.IntegerField()
	bullet_deal = models.IntegerField()
	booze = models.IntegerField()
	narcotics = models.IntegerField()
	##solo actions
	short_job = models.IntegerField()
	medium_job = models.IntegerField()
	long_job = models.IntegerField()
	##group actions
	heist = models.IntegerField()
	organised_crime = models.IntegerField()
	raid = models.IntegerField()
	mega_oc = models.IntegerField()
	smuggle = models.IntegerField()
	
	#action xp values
	short_job_xp = models.IntegerField()
	medium_job_xp = models.IntegerField()
	long_job_xp = models.IntegerField()
	heist_xp = models.IntegerField()
	organised_crime_xp = models.IntegerField()
	raid_xp = models.IntegerField()
	mega_oc_xp = models.IntegerField()
	booze_xp = models.IntegerField()
	narcotics_xp = models.IntegerField()
	
	
	#Booze base prices
	beer = models.IntegerField()
	cider = models.IntegerField()
	cognaq = models.IntegerField()
	rum = models.IntegerField()
	vodka = models.IntegerField()
	whiskey = models.IntegerField()
	wine = models.IntegerField()

	#narcotic base prices
	cocaine = models.IntegerField()
	tabacco = models.IntegerField()
	morphine = models.IntegerField()
	glue = models.IntegerField()
	amfetamines = models.IntegerField()
	heroin = models.IntegerField()
	cannabis = models.IntegerField()
	
	#smuggling modifiers
	price_difference = models.IntegerField()					# % of pricedeviation for booze and narc prices
	
	booze_min_chance = models.IntegerField()
	booze_max_chance = models.IntegerField()
	booze_try = models.IntegerField()							# every x gives 1% of extra chance
	booze_rank	= models.FloatField()							# times *rank as base chance
	booze_failed_min = models.IntegerField()					# min jail timer
	booze_failed_max = models.IntegerField()					# max jail timer
	booze_random = models.IntegerField()						#random amount
	
	narcotics_min_chance = models.IntegerField()
	narcotics_max_chance = models.IntegerField()
	narcotics_try = models.IntegerField()
	narcotics_rank = models.FloatField()
	narcotics_failed_min = models.IntegerField()
	narcotics_failed_max = models.IntegerField()
	narcotics_random = models.IntegerField()
	
	
	def __unicode__(self):
		return "Game Base Values"



class Housing(models.Model):
	""" house stats """
	
	HOUSE = "house"
	GARAGE = "garage"
	BASEMENT = "basement"
	GARDEN = "garden"
	HOUSETYPES = (
		(HOUSE, "house"),
		(GARAGE, "garage"),
		(BASEMENT, "basement"),
		(GARDEN, "garden"),
	)
		
	name = models.CharField(max_length=31)
	description = models.TextField()
	category = models.CharField(max_length=15, choices=HOUSETYPES)
	rank = models.IntegerField()
	price = models.IntegerField()
	defense = models.IntegerField()
	booze = models.IntegerField()
	narcotics = models.IntegerField()
	cars = models.IntegerField()
	
	class Meta:
		unique_together = ["name", "category"]
	
	
	def __unicode__(self):
		return "category: %s, name: %s" % (self.category, self.name)
	
	#view price in template
	def view_price(self):
		return convert_damn(self.price)
	
	#view rank for template (rendered in form)
	def view_rank(self):
		if self.rank < 4:
			return self.rank
		else:
			return "MAX"
			
	
	
	
	
	
	
	
	#returns the difference in storage space
	def storage_increase(self):
		#get previous rank of building or True
		try:
			current = Housing.objects.get(category=self.category, rank=self.rank-1)
		except ObjectDoesNotExist:
			current = True
		
		#the "storgae" spaces
		storage = OrderedDict()
		spaces = ['defense', 'booze', 'narcotics', 'cars']
		
		for space in spaces:
			#get the temp value of space
			temp = getattr(self, space)
			
			if temp > 0:
				if current == True:
					storage[space] = "+" + str(getattr(self, space))
				else:
					storage[space] = "+" + str(getattr(self, space) - getattr(current, space))
			
		return storage
			
			
			
		
		
		
		
		
	
	
	
		
class SinglePlayerJob(models.Model):
	""" jobs to get items or higher payou8t that take 5 mintes """
	
	SHORT = "short"
	MEDIUM = "medium"
	CATEGORIES = (
		(SHORT, "Short Job"),
		(MEDIUM, "Medium Job"),
	)
	
	flavor = models.CharField(max_length=127)
	category = models.CharField(max_length=7, choices=CATEGORIES)
	rarity = models.IntegerField()
	
	car = models.BooleanField(default=False)						# True if car can be looted
	gun = models.BooleanField(default=False)						# True if gun can be looted
	damn = models.BooleanField(default=False)					# True if damn can be earned
	
	chance_min = models.IntegerField()
	chance_max = models.IntegerField()
	chance_random = models.IntegerField()
	
	damn_min = models.IntegerField(null=True)						
	damn_max = models.IntegerField(null=True)
	damn_random = models.IntegerField(null=True)						#percent random
		
	def __unicode__(self):
		return self.flavor
		
	
	#get a random joblist 
	@staticmethod
	def get_job_list(character, category):
		all_jobs = SinglePlayerJob.objects.filter(category=category).exclude(rarity__exact=0)
		always = SinglePlayerJob.objects.filter(category=category, rarity=0)
		pick_list = []
		job_list = {}
		
		#job_list = []
		#JobSet = namedtuple("JobSet", "flavor chance")
		
		if category == SinglePlayerJob.SHORT:
			length = 5
		else:
			length = 4
		
		
		for job in all_jobs:
			pick_list.extend([job] * job.rarity)

		counter = 0
		while counter < length:
			counter += 1
			job = choice(pick_list)
			chance = get_min_max_result(job.chance_min, job.chance_max, job.chance_random, character.rank.rank)
			#job_list.append(JobSet(flavor=job.flavor, chance=chance))
			job_list[job.flavor] = chance
			
			while job in pick_list:
				pick_list.remove(job)

		for job in always:
			chance = get_min_max_result(job.chance_min, job.chance_max, job.chance_random, character.rank.rank)
			#job_list.append(JobSet(flavor=job.flavor, chance=chance))
			job_list[job.flavor] = chance
			
			
		return job_list



		
	# check if the job succeeds and take consequences based on result
	@staticmethod
	def check_to_succeed(flavor, chance, character):
		job = SinglePlayerJob.objects.get(flavor=flavor)
		
		#increase counter by 1
		if job.category == SinglePlayerJob.SHORT:
			character.short_jobs += 1
		elif job.category == SinglePlayerJob.MEDIUM:
			character.medium_jobs += 1
		
		character.save()
		
		#special jobs
		shoot = SinglePlayerJob.objects.get(flavor="Practice your acuracy with guns.")
		escort = SinglePlayerJob.objects.get(flavor="Pay an escort for oral sex.")
		prostitute = SinglePlayerJob.objects.get(flavor="Pay a prostitute to help you out with your needs.")
		steal_from_player = ["Pickpocket another mercenary.", "Steal gun from another mercanary.", "Steal a car from another mercenary."]
		steal = SinglePlayerJob.objects.filter(flavor__in=steal_from_player)
		drugdealer = SinglePlayerJob.objects.get(flavor="Rob a drugdealer on the street.")
		
		roll = randint(0, 100)

		
		# if you try practice accuracy
		if job == shoot:
			return SinglePlayerJob.practice_accuracy(chance, character)
		
		# if try to get an escort
		elif job == escort or job == prostitute:
			return SinglePlayerJob.escort_service(job, chance, character)
		
		#if you try to pickpocket
		elif job in steal:
			return SinglePlayerJob.steal_from_player(job, chance, character)
		
		# if you rob a drugdealer
		elif job == drugdealer:
			return SinglePlayerJob.drugdealer(job, chance, character)
		
		
		elif roll <= chance:
			#check what reward you get:
			results = {}
			
			if job.damn:
				damn = get_min_max_result(job.damn_min, job.damn_max, job.damn_random, character.rank.rank)
				character.update_damn(+ damn)
				
				results['succes'] = "Good job, you made %s out of it." % convert_damn(damn)
				
			elif job.car:
				car = random_object_by_model("car")
				add_car = CharacterCar(
					character=character,
					region=character.region,
					hitpoints=car.random_hp(),
					car=car,
				)
				add_car.save()
				
				flavor = "You managed to get yourself a %s. " % car.name
				if add_car.hitpoints < car.max_hitpoints:
					damage = 100-add_car.hp_percent()
					#TODO: add % before damage
					flavor += "However it took %s%% damage." % damage
				
				results['succes'] = flavor
				
			elif job.gun:
				gun = random_object_by_model("gun")
				add_gun = CharacterGun(
					character=character,
					region=character.region,
					gun=gun,
				)
				add_gun.save()
				
				results['succes'] = "You managed to get yourself a %s." % gun.name
			
			return results
				
		else:
			failed = random_object_by_model("failedsingleplayerjob", job=job)
			return failed.failed_job(character)



	#special job: Mechanics for training accuracy
	@staticmethod
	def practice_accuracy(chance, character):
		roll = randint(0,100)
		results = {}
		
		if roll <= chance:
			if character.accuracy < 10000:																#if players accuracy is below 100%
				character.accuracy += 1
				results['succes'] = "Good job! You hit your target and improved your accuracy."
			elif character.accuracy < 15000 and character.accuracy >=10000:								#if players accuracy is below 150%
				character.accuracy += 1
				results['succes'] = "You shot your target. Not sure if you can get any better though."
			else:																						#players accuracy to high
				results['succes'] = "Hitting a target is of no challenge to you anymore. This feels like wasting time."
			
			character.save()
			return results
		else:
			results['failed'] = "You did not manage to hit your target and did not improve your accuracy."
			return results



	#special job: Mechanics for getting blown
	@staticmethod
	def escort_service(job, chance, character):
		roll = randint(0, 100)
		cost = get_min_max_result(job.damn_min, job.damn_max, job.damn_random, character.rank.rank)
		results = {}
		
		#on succes you always pay for your try even if you dont get hp.
		if roll <= chance:
			if character.check_damn(cost):
				
				#check if small or medium job
				if job.category == SinglePlayerJob.MEDIUM:
					health = character.percent_health() * 3 + character.hitpoints
				else:
					health = character.percent_health() + character.hitpoints
				

				if health <= character.max_health():
					character.hitpoints += character.percent_health()
				else:
					character.hitpoints = character.max_health()
				
				character.update_damn(- cost)
				results['succes'] = "After almost 30 minutes of pure pleasure you feel refreshed. However you had to pay %s for it." % convert_damn(cost)
				
			else:
				character.damn = 0
				results['failed'] = "After you realised the price would be %s. The escort left you with the job unfinnished and your wallet empty." % convert_damn(cost)
			
			character.save()
			return results
		
		# on failed try you still have a 40% chance of paying and going to jail
		else:
			busted_roll = randint(0, 100)
			
			if busted_roll <= 40:
				# create jail timer
				if job.category == SinglePlayerJob.MEDIUM:
					timer = get_min_max_result(180, 520, 30, character.rank.rank)
				else:
					timer = get_min_max_result(40, 180, 30, character.rank.rank)
					
				character.charactertimers.update_timer(field="inactive", timer=timer, inactive="jail")
				
				character.update_damn(- cost)
				results['failed'] = "At the moment you paid your escort you get arrested and are in jail for %s. Even worse, they kept your %s!" % (convert_timedelta(timedelta(seconds=timer)), convert_damn(cost))
				
				if character.damn < 0:
					character.damn = 0
					results['failed'] = "After the escort took everything from your wallet, she turned out to be a cop and you got arrested for %s." % convert_timedelta(timedelta(seconds=timer))
					
				character.save()
				return results
				
			else:
				results['failed'] = "There where no free escorts to be sent your way at this time of the day."
				return results


	
	##Special Job: Pickpocket something from another mercenary:
	@staticmethod
	def steal_from_player(job, chance, character):
		#random a character to stealfrom you excluded.
		results = {}
		try:
			target = Character.objects.filter(region=character.region).exclude(user=character.user, alive=True).order_by('?')[0]
		except IndexError:
			flavor = "You are the only mercenary in this region. Can't steal from yourself"
			results['failed'] = flavor
			return results
		
		roll = randint(0, 100)
		
		if roll <= chance:
			# see if you are pickpocketing, or stealign a car or gun
			if job.category == SinglePlayerJob.SHORT:
				job_type = "pickpocket"
				steal = get_min_max_result(job.damn_min, job.damn_max, job.damn_random, character.rank.rank)
				
				
				#see if target has enough money, otherwise steal what he has.
				if target.check_damn(steal):
					target.update_damn(- steal)
					character.update_damn(steal)
					
				else:
					steal = target.damn
					target.damn = 0
					character.update_damn(steal)
					
				
				target.save()
				character.save()
				
				#TODO: change charactername to link to character profile.
				flavor = "You managed to steal %s from %s!" % (convert_damn(steal), target)
				
			elif job.category == SinglePlayerJob.MEDIUM:
				if "car" in job.flavor:
					job_type = "car"
					try:
						car = CharacterCar.objects.filter(region= character.region, safe=False).exclude(character=character).order_by('?')[0]
					except IndexError:
						flavor = "There are no cars to steal here except your own."
						results['failed'] = flavor
						return results
					
					#TODO: change charactername to link to character profile.
					flavor = "You managed to steal a %s from %s!" % (car.car.name, car.character.name)
					target = car.character
					
					#change owner of the stolen car
					car.character = character
					car.save()
					
				elif "gun" in job.flavor:
					job_type = "gun"
					try:
						gun = CharacterGun.objects.filter(region= character.region, safe=False).exclude(character=character).order_by('?')[0]
					except IndexError:
						flavor = "There are no guns to steal here except your own."
						results['failed'] = flavor
						return results
					
					#TODO: change charactername to link to character profile.
					flavor = "You managed to steal a %s from %s!" % (gun.gun.name, gun.character.name)
					target= gun.character
					
					#change owner of the stolen car
					gun.character = character
					gun.save()
			
			
			#get difference in rank and get chance to get caught
			rank = target.rank.rank - character.rank.rank
			if rank < 1:
				rank = 1
			
			caught_chance = get_min_max_result(job.chance_min, job.chance_max, job.chance_random, rank)
			caught_roll = randint(0, 100)
			
			#check if target caught the culprit
			if caught_roll <= caught_chance:
				flavor += " However your target caught you and will be notified."
				
				#TODO: create links to view character and stolen goods
				to_character = target
				category = Mail.NOTIFICATION
				
				if job_type == "pickpocket":
					subject = "Some damn got stolen!"
					body = "%s mangaged to steal %s damn from you." % (character, steal)
				elif job_type == "car":
					subject = "A car has been stolen!"
					body = "%s mangaged to steal a %s from you." % (character, car.car.name)
				elif job_type == "gun":
					subject = "A gun has been stolen!"
					body = "%s mangaged to steal a %s from you." % (character, gun.name)
					
				Mail.send_mail(to_character, category, subject, body)
			
			results['succes'] = flavor
			return results
		
		
		#if action fails:
		else:
			failed = random_object_by_model("failedsingleplayerjob", job=job)
			return failed.failed_job(character)
			
	
	
	
	def drugdealer(job, chance, character):
		loot = ['damn', 'car', 'gun']
		shuffle(loot)
		flavor = ""
		results = {}
		
		for item in loot:
			roll = randint(0, 100)
			
			if roll <= chance:
				if item == "damn":
					reward = get_min_max_result(job.damn_min, job.damn_max, job.damn_random, character.rank.rank)
					character.update_damn(reward)
					flavor = "Good job, you made %s out of it.<br>" % convert_damn(reward)
					if 'succes' in results:
						results['succes'] += flavor
					else:
						results['succes'] = flavor
					
				elif item == "car":
					car = random_object_by_model("car")
					add_car = CharacterCar(
						character=character,
						region=character.region,
						hitpoints=car.random_hp(),
						car=car,
					)
					add_car.save()
				
					flavor = "You managed to get yourself a %s." % car.name
					if add_car.hitpoints < car.max_hitpoints:
						damage = 100 - add_car.hp_percent()
						flavor += " However it took %s%% damage.<br>" % damage
					else:
						flavor += "<br>"
					
					flavor += "\n"
					if 'succes' in results:
						results['succes'] += flavor
					else:
						results['succes'] = flavor
					
					
					
				elif item == "gun":
					gun = random_object_by_model("gun")
					add_gun = CharacterGun(
						character=character,
						region=character.region,
						gun=gun,
					)
					add_gun.save()
				
					flavor = "You managed to get yourself a %s.<br>" % gun.name
					
					if 'succes' in results:
						results['succes'] += flavor
					else:
						results['succes'] = flavor
			
			else:
				failed = random_object_by_model("failedsingleplayerjob", job=job)
				temp = failed.failed_job(character)
				results['failed'] = temp['failed']	
				return results
		
		return results
		
		
		
	

class FailedSinglePlayerJob(models.Model):
	""" Failed messages and possible hospital/jail timers """
	
	job = models.ForeignKey(SinglePlayerJob)
	flavor = models.CharField(max_length=127, unique=True)
	rarity = models.IntegerField()
	legal = models.BooleanField()
	
	timer = models.BooleanField()
	timer_min = models.IntegerField(null=True)
	timer_max = models.IntegerField(null=True)
	timer_random = models.IntegerField(null=True)
	
	def __unicode__(self):
		return self.flavor
		
		
	# return message + possible jail/hospital settings after a failed job
	def failed_job(self, character):
		results = {}

		if self.timer:
			timer = get_min_max_result(self.timer_min, self.timer_max, self.timer_random, character.rank.rank)
			timer_string = convert_timedelta(timedelta(seconds=timer))
			flavor = self.flavor.replace("TIMER", timer_string)
			if self.legal:
				inactive = "hospital"
			else:
				inactive = "jail"
			
			character.charactertimers.update_timer(field="inactive", timer=timer, inactive=inactive)
			results['failed'] = flavor
			return results
		
		results['failed'] = self.flavor
		return results
