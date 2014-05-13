from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import utc

from elements.models import Rank, Region, GameBaseValues, Transport
from elements.models import TravelMethod, Car, Gun, Armor
from elements.models import get_min_max_result, convert_damn, convert_timedelta

from datetime import datetime, timedelta
from random import randint
from collections import OrderedDict, namedtuple



class Character(models.Model):
	""" User characters that hold the personal game stats """

	created = models.DateTimeField(auto_now_add=True)
	alive = models.BooleanField(default=True)
	user = models.OneToOneField(User, unique=True)
	
	rank = models.ForeignKey(Rank)
	region = models.ForeignKey(Region)
	alliance = models.ForeignKey('Alliance', null=True)
	
	damn = models.IntegerField(default=0)
	banked = models.IntegerField(default=0)
	
	transport = models.ForeignKey(TravelMethod)
	gun = models.CharField(max_length=31, default="None") 
	bullets = models.IntegerField(default=0)
	
	short_jobs = models.IntegerField(default=0)
	medium_jobs = models.IntegerField(default=0)
	long_jobs = models.IntegerField(default=0)
	races_done = models.IntegerField(default=0)
	races_won = models.IntegerField(default=0)
	kills = models.IntegerField(default=0)
	
	
	hitpoints = models.IntegerField()
	accuracy = models.IntegerField(default=0)
	xp = models.IntegerField(default=0)
	booze_tries = models.IntegerField(default=0)
	drugs_tries = models.IntegerField(default=0)
	
	def __unicode__(self):
		return self.user.username
	
	
	@staticmethod	
	def create(user):
		region_id = randint(1, Region.objects.all().count())
		
		new_character = Character(
			user=user,
			region=Region.objects.get(id=region_id),
			rank=Rank.objects.get(name="Cadet"),					#hardcoded lowest rank
			hitpoints=Rank.objects.get(name="Cadet").hitpoints,
			transport=TravelMethod.objects.get(name='Hitchhike'),
		)
		new_character.save()
		
		timers = CharacterTimers(
			character = new_character,
		)
		timers.save()
		
		#create means of transport
		CharacterTransport.create_transport(new_character)
		
	
	
	# return players basic information
	def basic_information(self):
		basic = OrderedDict()
		basic["name"] = self.user
		basic["start date"] = self.created
		basic["rank"] = self.rank
		basic["alliance"] = self.alliance
		basic["region"] = self.region
		
		return basic
	
	
	# return player possessions
	def possessions(self):	
		possessions = OrderedDict()
		#set currency
		
		possessions['damn'] = convert_damn(self.damn)
		possessions["transport"] = self.transport
		possessions["gun"] = self.gun
		possessions["bullets"] = self.bullets
		
		return possessions
		
		
	#return player status bars
	def status(self):
		status = OrderedDict()
		status["rank"] = self.view_rank_progress()
		status["healt"] = self.view_health()
		status['accuracy'] = self.view_accuracy()
		
		return status
	
	#return players woork experience
	def work_experience(self):
		work = OrderedDict()
		work["short jobs"] = self.short_jobs
		work["medium jobs"] = self.medium_jobs
		work["long jobs"] = self.long_jobs
		work["car races"] = self.races_done
		work["kills"] = self.kills
		
		return work
		
		

	# check if you got enough xp to get to next rank
	def check_rank(self):
		if self.xp > self.rank.max_xp:
			self.update_rank()
		
	
	
	# set character rank 
	def update_rank(self):
		#TODO put in allaince/capo ranks
		
		remove_ranks = ['Field Marshall', 'Military Attache', 'Mercenary Recruiter', 'Marshall']
		ranks = Rank.objects.exclude(special=True)
		
		for rank in ranks:
			if rank.min_xp <= self.xp and rank.max_xp >= self.xp:
				self.rank = rank
				self.hitpoints = self.rank.hitpoints
				self.save()
				return
		
	
	
	#get rank progres
	def view_rank_progress(self):
		needed_xp = self.rank.max_xp - self.rank.min_xp + 1.0
		got_xp = self.xp - self.rank.min_xp + 0.0
		procent = got_xp / needed_xp * 100
		return "%.2f %%" % procent
	
	
	# get % health
	def view_health(self):
		health = (self.hitpoints + 0.0) / (self.rank.hitpoints) * 100
		if health > 100:
			health = 100
		return "%.2f %%" % health
	
	#get 1% of total health based on rank
	def percent_health(self):
		percent = int(self.rank.hitpoints / 100)
		if percent < 1:
			percent = 1
		return percent
		
	# get max hitpoints	
	def max_health(self):
		return int(self.rank.hitpoints * 1.1)
	
		
	# get players view of accuracy
	def view_accuracy(self):
		accuracy = (self.accuracy + 0.0) / 100
		if accuracy > 100:
			accuracy = 100.00
		return "%.2f %%" % accuracy
		
		
	
			
	#set new xp, and timer
	def perform_action(self, field):
		self.charactertimers.update_timer(field=field)
				
		#add xp
		values = GameBaseValues.objects.get(id=1)
		setattr(self, "xp", self.xp + getattr(values, field+"_xp"))
		self.save()
		
		#check if you ranked up
		self.check_rank()
		

	
	
class CharacterTimers(models.Model):
	""" To keep track of timers of a character """
	
	now = datetime.utcnow().replace(tzinfo=utc)
	
	character = models.OneToOneField(Character)
	
	#normal actions
	travel = models.DateTimeField(default=now)					#timer depends on plane,  default = 2 hours(no plane)
	blood = models.DateTimeField(default=now)					#1 hour timer
	race = models.DateTimeField(default=now)					#30 minutes
	kill = models.DateTimeField(default=now)					#1 hour timer
	bullet_deal = models.DateTimeField(default=now)				#1 hour timer
	booze = models.DateTimeField(default=now)					#every 30 minutes available for xp
	drugs = models.DateTimeField(default=now)					#every 30 minutes available for xp
	
	#solo actions
	short_job = models.DateTimeField(default=now)				#1 minute 30 seconds
	medium_job = models.DateTimeField(default=now)				#5 minutes
	long_job = models.DateTimeField(default=now)				#15 minutes
	
	#group actions
	heist = models.DateTimeField(default=now)					#3 hour timer	(rob some random things)
	organised_crime = models.DateTimeField(default=now)			#6 hour timer	(rob a bank)
	raid = models.DateTimeField(default=now)					#12 hour timer	(help army on mission)
	mega_oc = models.DateTimeField(default=now)					#24 hour timer 	(rob a national bank or other big place)	
	
	#jail timers
	location = models.NullBooleanField(default=True)			#True for active, False for in jail, None for in hospital
	inactive = models.DateTimeField(default=now)				#time you are held up in hospital or jail
	
	def __unicode__(self):
		return "%s's timers" % self.character.user.name
		
	
	def timers(self):
		fields = OrderedDict()
		fields["short job"] = ""
		fields["medium job"] = ""
		fields["long job"] = ""
		fields["booze"] = ""
		fields["drugs"] = ""
		fields["heist"] = ""
		fields["organised crime"]= ""
		fields["raid"] = ""
		fields["mega oc"] = ""
		fields["travel"] = ""
		fields["blood"] = ""
		fields["race"] = ""
		fields["kill"] = ""
		fields["bullet deal"] = ""
		
		now = datetime.utcnow().replace(tzinfo=utc)

		Link = namedtuple("Link", "url timer")
		group_crimes = ("heist", "organised crime", "mega oc", "raid")
		
		for field in fields:			
			timer = getattr(self, field.replace(" ", "_"))
						
			if field == "booze" or field == "drugs":
				url = "contraband"
			elif field in group_crimes:
				url = "group crime"
			else:
				url = field
			
			#field.replace("_", " ")
			if now > timer:
				fields[field] = Link(url=url, timer="Now")
			else:
				fields[field] = Link(url=url, timer=convert_timedelta(timer - now))
		
		return fields

			
	
	# get timer by field
	def check_timer(self, field):
		timer = getattr(self, field)
		now = datetime.utcnow().replace(tzinfo=utc)
		
		TimerCheck = namedtuple("TimerCheck", "check timer")
		
		#check if in jail/hospital
		if self.inactive < now:
			self.location=True
			self.save()
		elif self.location == False:
			timer = "You are still locked up in jail for %s." % convert_timedelta(self.inactive - now)
			return TimerCheck(check=False, timer=timer)
		elif self.location == None:
			timer = "You are getting patched up in hospital. Please wait another %s" % convert_timedelta(self.inactive - now)
			return TimerCheck(check=False, timer=timer)
			
		if now > timer:
			return TimerCheck(check=True, timer="Now")
		else:
			timer = "You are still tired from your last job. please wait another %s before trying again." % convert_timedelta(timer - now)
			return TimerCheck(check=False, timer=timer)


	def check_if_inactive(self):
		now = datetime.utcnow().replace(tzinfo=utc)
		
		if self.inactive < now:
			self.location=True
			self.save()
	
	
	#set a timer
	def update_timer(self, field, **kwargs):
		values = GameBaseValues.objects.get(id=1)
		if 'timer' in kwargs:
			timer = timedelta(seconds=kwargs['timer'])
		else:
			timer = timedelta(seconds=getattr(values, field))
		
		#set nullboolean to hospital or jail
		if "inactive" in kwargs:
			if kwargs['inactive'] == "jail":
				self.location = False
			elif kwargs['inactive'] == "hospital":
				self.location = None
			else:
				print "no suitable result for inactive!!!"
		
		#set timer
		now = datetime.utcnow().replace(tzinfo=utc)
		setattr(self, field, now + timer)
		self.save()
		
	


class CharacterTransport(models.Model):
	""" regions player and there means of transport """
	
	character = models.ForeignKey(Character)
	region = models.ForeignKey(Region)
	transport = models.ForeignKey(Transport, null=True, blank=True)
	
	class Meta:
		unique_together = ("character", "region")
		
	def __unicode__(self):
		return "%s %s %s" % (self.character, self.region, self.transport)
		
	
	@staticmethod
	def create_transport(character):
		regions = Region.objects.all()
		for region in regions:
			new_transport = CharacterTransport(
				character=character,
				region=region,
			)
			new_transport.save()
			
	
	# zou classmethod moeten zijn?
	@staticmethod
	def transport_overview(character):
		chartransports = CharacterTransport.objects.filter(character=character).order_by('region__name')
		overview = OrderedDict()
		
		for chartransport in chartransports:
			if chartransport.transport == None:
				overview[chartransport.region.name] = "Available"
			else:
				overview[chartransport.region.name] = chartransport.transport.name
		
		return overview
	


class CarPercentManager(models.Manager):
	def hp_percent(self):
		return int(self.hitpoints / (self.car.hitpoints / 100 + 0.0))


class CarRepairCostManager(models.Manager):
	def repair_cost(self):
		to_repair = 100 - int(self.hitpoints / (self.car.hitpoints / 100 + 0.0))
		price = int((self.car.price /100 +0.0) * to_repair)
		return price


class CharacterCar(models.Model):
	""" cars a character owns plus the location they are in """
	
	character = models.ForeignKey(Character)
	
	car = models.ForeignKey(Car)
	region = models.ForeignKey(Region)
	hitpoints = models.IntegerField()
	hp_percent = CarPercentManager()
	repaircost = CarRepairCostManager()
	
	def __unicode__(self):
		return "%s: %s" % (self.character, self.car)
		



class CharacterGun(models.Model):
	""" cars a character owns plus the location they are in """
	
	character = models.ForeignKey(Character)
	
	gun = models.ForeignKey(Gun)
	region = models.ForeignKey(Region)
	
	def __unicode__(self):
		return "%s: %s" % (self.character, self.gun)
		
		
		

class CharacterArmor(models.Model):
	""" cars a character owns plus the location they are in """
	
	character = models.ForeignKey(Character)
	
	armor = models.ForeignKey(Armor)
	region = models.ForeignKey(Region)
	
	def __unicode__(self):
		return "%s: %s" % (self.character, self.armor)
	



class Alliance(models.Model):
	""" alliances to handle player groups their assets etc """
	
	name = models.CharField(max_length=63, unique=True)
	profile = models.TextField()
	
	leader = models.ForeignKey(Character, related_name="leader")
	diplomat = models.ForeignKey(Character, related_name="diplomat")
	recruiter = models.ForeignKey(Character, related_name="recruiter")
	successor = models.ForeignKey(Character, related_name="successor")
	
	def __unicode__(self):
		return self.name
		
		
		
class Location(models.Model):
	""" locations are bound to Regions and are "territory" for alliances """
	
	DEFENSIVE = "def"
	OFFENSIVE = "off"
	CONTRABAND = "con"
	HOSPITAL = "hos"
	JAIL = "jail"
	LOCATION_CATEGORIES = (
		(DEFENSIVE, "Defensive"),
		(OFFENSIVE, "Offensive"),
		(CONTRABAND, "Contraband"),
		(HOSPITAL, "Hospital"),
		(JAIL, "Jail"),
	)
	
	name = models.CharField(max_length=31, unique=True)
	category = models.CharField(max_length=3, choices=LOCATION_CATEGORIES)
	
	region = models.ForeignKey(Region)
	alliance = models.ForeignKey(Alliance, null=True)
	owner = models.ForeignKey(Character, null=True)
	
	def __unicode__(self):
		return self.name
