from django.db import models

from random import randint, choice
from collections import namedtuple, OrderedDict
from datetime import datetime, timedelta

#convert damn to currency
def convert_damn(damn):
	return '{:,}'.format(damn) + " Dmn"


#File upload name maker
def get_upload_file_name(instance, filename):
	return "uploaded_portraits/%s_%s" % (str(time()).replace('.','_'), filename)


#get result for min/max/random equation
def get_min_max_result(minimum, maximum, chance, character):
	# Example: minimum = 15, maximum = 50, chance = 40, character.rank.rank = 5
	# max_ranks = 12
	# base = (50 - 15)/ 12 * 5 = 14.58
	# char_base = 14.58 / 100 * (100 - 40) = 8.75
	# rand_base // 14.58 - 8.75 = 5.83 // random between 0 and 5 (integer) = 3
	# total = integer of 15 + 14.58 + 3 = 32
	
	max_ranks = Rank.objects.all().count() - 2									#-2 for the special alliance ranks
	base = (maximum - minimum + 0.0) / max_ranks * character.rank.rank			
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
		string += "{}H ".format(hours)
	if minutes > 0:
		string += "{}M ".format(minutes)
	if seconds > 0:
		string += "{}S ".format(seconds)
	
	return string




# Named tupple to return job results
# check = True, job succeed. check=False, job failed. check=None, you are busted 
# busted = True, in jail. busted=False in hospital
class Results(namedtuple('Results', "check busted flavor")):
	def __new__(cls, check, busted=None, flavor=""):
		return super(Results, cls).__new__(cls, check, busted, flavor)

	


class Rank(models.Model):
	""" Ranks with their stats """
	
	name = models.CharField(max_length=31, unique=True)
	rank = models.IntegerField()
	min_xp = models.IntegerField()
	max_xp = models.IntegerField()
	hitpoints = models.IntegerField()
	booze = models.IntegerField()
	narcotics = models.IntegerField()
	
	def __unicode__(self):
		return self.name

	
	
class Plane(models.Model):
	""" all plane types you can buy in market """
	
	name = models.CharField(max_length=63, unique=True)
	travel_timer = models.IntegerField()								# in seconds
	image = models.FileField(upload_to=get_upload_file_name, null=True)
	
	def __unicode__(self):
		return self.name
	


class Gun(models.Model):
	""" all different guns available in game """
	
	rarity = models.IntegerField()
	image = models.FileField(upload_to=get_upload_file_name, null=True)
	
	brand = models.CharField(max_length=63, unique=True)
	model = models.CharField(max_length=127, unique=True)
	
	damage = models.FloatField()
	magazine = models.IntegerField()
	
	
	def __unicode__(self):
		return self.name



class Car(models.Model):
	""" all different cars available in game """
	
	image = models.FileField(upload_to=get_upload_file_name, null=True)
	
	rarity = models.IntegerField()
	brand = models.CharField(max_length=63, unique=True)
	model = models.CharField(max_length=127, unique=True)
	
	speed = models.IntegerField()
	hitpoints = models.IntegerField()
	seats = models.IntegerField()
	
	def __unicode__(self):
		return self.name


	
class Region(models.Model):
	""" type of booze and their base price """
	
	name = models.CharField(max_length=31, unique=True)
	alliance_slots = models.IntegerField()					#Maximum amounts of alliances in this region
	
	#base contraband prices
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
		return self.name
	
		

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
	drugs = models.IntegerField()
	##solo actions
	short_job = models.IntegerField()
	medium_job = models.IntegerField()
	long_job = models.IntegerField()
	##group actions
	heist = models.IntegerField()
	organised_crime = models.IntegerField()
	raid = models.IntegerField()
	mega_oc = models.IntegerField()
	
	#action xp values
	short_job_xp = models.IntegerField()
	medium_job_xp = models.IntegerField()
	long_job_xp = models.IntegerField()
	heist_xp = models.IntegerField()
	organised_crime_xp = models.IntegerField()
	raid_xp = models.IntegerField()
	mega_oc_xp = models.IntegerField()
	booze_xp = models.IntegerField()
	drugs_xp = models.IntegerField()
	
	
	#Booze base prices
	beer = models.IntegerField()
	cider = models.IntegerField()
	cognaq = models.IntegerField()
	rum = models.IntegerField()
	vodka = models.IntegerField()
	whiskey = models.IntegerField()
	wine = models.IntegerField()

	#Drug base prices
	cocaine = models.IntegerField()
	tabacco = models.IntegerField()
	morphine = models.IntegerField()
	glue = models.IntegerField()
	amfetamines = models.IntegerField()
	heroin = models.IntegerField()
	cannabis = models.IntegerField()
	
	def __unicode__(self):
		return "Game Base Values"



class ShortJob(models.Model):
	""" jobs that only take 1 min 30 seconds """
	
	name = models.CharField(max_length=127, unique=True)
	rarity = models.IntegerField()
	legal = models.BooleanField()							#legal player goes to hospital, false to jail						
	
	damn_min = models.IntegerField()						
	damn_max = models.IntegerField()
	damn_random = models.IntegerField()						#percent random
	
	chance_min = models.IntegerField()
	chance_max = models.IntegerField()
	chance_random = models.IntegerField()
	
	#failure stats:
	timer = models.BooleanField()						#True if player goes to hospital or jail
	timer_min = models.IntegerField(null=True)
	timer_max = models.IntegerField(null=True)
	timer_random = models.IntegerField(null=True)
	
	def __unicode__(self):
		return self.name
		
	
	#get a random joblist 
	@staticmethod
	def get_job_list(character):
		all_jobs = ShortJob.objects.exclude(rarity__exact=0)
		always = ShortJob.objects.filter(rarity=0)
		pick_list = []
		job_list = OrderedDict()

		for job in all_jobs:
			pick_list.extend([job] * job.rarity)

		counter = 0
		while counter < 5:
			counter += 1
			job = choice(pick_list)
			#job_list[job.name] = ShortJob.succes_chance(character, job)
			job_list[job.name] = get_min_max_result(job.chance_min, job.chance_max, job.chance_random, character)
			
			while job in pick_list:
				pick_list.remove(job)

		for job in always:
			#job_list[job.name] = ShortJob.succes_chance(character, job)
			job_list[job.name] = get_min_max_result(job.chance_min, job.chance_max, job.chance_random, character)

		return job_list
	
	
	
	@staticmethod
	def practice_accuracy(chance, character):
		roll = randint(0,100)
		
		if roll <= chance:
			if character.accuracy < 10000:																#if players accuracy is below 100%
				character.accuracy += 1
				flavor = "Good job! You hit your target and improved your accuracy."
			elif character.accuracy < 15000 and character.accuracy >=10000:								#if players accuracy is below 150%
				character.accuracy += 1
				flavor = "You shot your target. Not sure if you can get any better though."
			else:																						#players accuracy to high
				flavor = "Hitting a target is of no challenge to you anymore. This feels like wasting time."
			
			character.save()
			return Results(check=True, flavor=flavor)
		else:
			flavor = "You did not manage to hit your target and did not improve your accuracy."
			return Results(check=False, flavor=flavor)
				
		
		
	@staticmethod
	def escort_service(chance, character):
		escort = ShortJob.objects.get(name="Pay an escort for oral sex.")
		roll = randint(0, 100)
		cost = get_min_max_result(escort.damn_min, escort.damn_max, escort.damn_random, character)
		
		#on succes you always pay for your try even if you dont get hp.
		if roll <= chance:
			if character.damn >= cost:
				if character.percent_health() + character.hitpoints <= character.max_health():
					character.hitpoints += character.percent_health()
				else:
					character.hitpoints = character.max_health()
				
				character.damn -= cost
				flavor = "After almost 30 minutes of pure pleasure you feel refresht. However you had to pay %s for it." % convert_damn(cost)
				
			else:
				character.damn = 0
				flavor = "After you realised the price would be %s. The escort left you with the job unfinnished and your wallet empty." % convert_damn(cost)
			
			character.save()
			return Results(check=True, flavor=flavor)
		
		# on failed try you still have a 40% chance of paying and going to jail
		else:
			busted_roll = randint(0, 100)
			
			if busted_roll <= 40:
				# create jail timer
				timer = get_min_max_result(escort.timer_min, escort.timer_max, escport.timer_random, character)
				character.charactertimers.update_timer(field="inactive", timer=timer, inactive="jail")
				
				character.damn -= cost
				flavor = "At the moment you paid your escort you get arrested and are in jail for %s. Even worse, they kept your %s!" % convert_timedelta(timedelta(seconds=timer))
				if character.damn < 0:
					character.damn = 0
					flavor = "After the escort took everything from your wallet, you got arrested for %s." % convert_timedelta(timedelta(seconds=timer))
					
				character.save()
				return Results(check=None, busted=True, flavor=flavor)
				
			else:
				flavor = "There where no free escorts to be sent your way at this time of the day."
				return Results(check=False, flavor=flavor)
	
	
	
	
	# check if the job succeeds and take consequences based on result
	@staticmethod
	def check_to_succeed(name, chance, character):
		job = ShortJob.objects.get(name=name)
		shoot = ShortJob.objects.get(name="Practice your acuracy with guns.")
		escort = ShortJob.objects.get(name="Pay an escort for oral sex.")
		roll = randint(0,100)
		
		# if succeed on shooting bottle
		if job == shoot:
			return ShortJob.practice_accuracy(chance, character)
		
		# if you succeed on getting an escort
		elif job == escort:
			return ShortJob.escort_service(chance, character)
		
		#	
		elif roll <= chance:
			#get reward in damn
			reward = get_min_max_result(job.damn_min, job.damn_max, job.damn_random, character)
			#add to character
			character.damn += reward
			character.save()
			flavor = "You where succesfull at your job and made %s out of it!" % convert_damn(reward)
			return Results(check=True, flavor=flavor)
		else:
			# see if you can end up in hospital or jail.
			if job.timer:
				timer = get_min_max_result(job.timer_min, job.timer_max, job.timer_random, character)
				#check if jail or hospital
				if job.legal:
					inactive = "hospital"
					flavor = "You got injured and ended up in hospital for %s." % convert_timedelta(timedelta(seconds=timer))
					busted = False
				else:
					inactive = "jail"
					flavor = "You got busted and got jailed for %s." % convert_timedelta(timedelta(seconds=timer))
					busted = True
					
				character.charactertimers.update_timer(field="inactive", timer=timer, inactive=inactive)
				return Results(check=False, busted=busted, flavor=flavor)
			else:
				if job.legal:
					flavor = "You messed up and didn't get paid"
				else:
					flavor = "You failed but got away."	
				
				return Results(check=False, flavor=flavor)
				
	
	
	

			
			
			
			
		
	
	
class MediumJob(models.Model):
	""" jobs to get items or higher payou8t that take 5 mintes """
	
	rarity = models.IntegerField()
	flavor = models.CharField(max_length=127)
	legal = models.BooleanField()
	
	failed = models.FloatField()					# basenumber to get time in hospital/jail
	car = models.BooleanField()						# True if car can be looted
	gun = models.BooleanField()						# True if gun can be looted
	credit = models.BooleanField()					# True if credits can be earned
	
	base_credit = models.FloatField()
	base_succes = models.FloatField()				# base multiplier for succes chance
	min_chance = models.IntegerField()
	max_chance = models.IntegerField()
	
	def __unicode__(self):
		return self.flavor
