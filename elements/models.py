from django.db import models

from random import randint, choice
from collections import namedtuple, OrderedDict


#File upload name maker
def get_upload_file_name(instance, filename):
	return "uploaded_portraits/%s_%s" % (str(time()).replace('.','_'), filename)


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
	legal = models.BooleanField()							
	
	damn_min = models.IntegerField()						
	damn_max = models.IntegerField()
	damn_random = models.IntegerField()						#percent random
	
	chance_min = models.IntegerField()
	chance_max = models.IntegerField()
	chance_random = models.IntegerField()
	
	#get_job_list = ShortJobManager()
	
	def __unicode__(self):
		return self.name
		
	
	# get the player chance from a job
	@staticmethod
	def succes_chance(character, job):
		times_rank = (job.chance_max - job.chance_min + 0.0) / (Rank.objects.all().count() - 2 )			#get rank modifier
		solid_chance = int(times_rank * character.rank.rank + job.chance_min)								#get solid chance based on rank
		random_chance = randint(job.chance_min -solid_chance, job.chance_max - solid_chance)				#get the random amount
		total = random_chance + solid_chance
		return total
	

	
	
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
			job_list[job.name] = ShortJob.succes_chance(character, job)
			
			while job in pick_list:
				pick_list.remove(job)

		for job in always:
			job_list[job.name] = ShortJob.succes_chance(character, job)

		return job_list
	
	
			
		

	
class ShotJobFail(models.Model):
	""" Fail messages on short jobs (When you dont go to jail/hospital """
	
	shortjob = models.ForeignKey(ShortJob)
	flavor = models.CharField(max_length=127)
	
	#Possible time in jail or hospital
	failed = models.BooleanField()							# true if jail or hospitaltime is involved
	failed_min = models.IntegerField(null=True)				# basenumber to get time in hospital/jail
	failed_max = models.IntegerField(null=True)
	#failed_random= models.IntegerField()					# always 50%
	
	# possible damage to hitpoints
	damage = models.BooleanField()
	damage_min = models.IntegerField(null=True)
	damage_max = models.IntegerField(null=True)
	damage_random = models.IntegerField(null=True)
	
	def __unicode__(self):
		return self.flavor
	

	
	
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
