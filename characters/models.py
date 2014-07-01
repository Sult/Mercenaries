from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import utc
from django.core.exceptions import ObjectDoesNotExist

import elements
import mail

from datetime import datetime, timedelta
from random import randint
from collections import OrderedDict, namedtuple






class Character(models.Model):
	""" User characters that hold the personal game stats """

	created = models.DateTimeField(auto_now_add=True)
	alive = models.BooleanField(default=True)
	user = models.ForeignKey(User)
	name = models.CharField(max_length=31, unique=True)
	
	rank = models.ForeignKey('elements.Rank')
	region = models.ForeignKey('elements.Region')
	alliance = models.ForeignKey('Alliance', null=True)
	
	damn = models.IntegerField(default=0)
	banked = models.IntegerField(default=0)
	
	transport = models.ForeignKey('elements.TravelMethod')
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
	narcotics_tries = models.IntegerField(default=0)
	
	class Meta:
		unique_together =['user', 'alive']
	
	def __unicode__(self):
		return self.name
	
	
	@staticmethod	
	def create(user, name):
		region = elements.models.Region.objects.all().order_by('?')[0]
		
		new_character = Character(
			user=user,
			name=name,
			region=region,
			rank=elements.models.Rank.objects.get(name="Cadet"),					#hardcoded lowest rank
			hitpoints=elements.models.Rank.objects.get(name="Cadet").hitpoints,
			transport=elements.models.TravelMethod.objects.get(name='Hitchhike'),
		)
		new_character.save()
		
		timers = CharacterTimers(
			character = new_character,
		)
		timers.save()
		
		#create means of transport
		CharacterTransport.create_transport(new_character)
		
		#create contraband
		CharacterContraband.create(new_character)
		
		#create mailbox
		mail.models.MailFolder.create_standard_folders(new_character)
		
	
	
	# return players basic information
	def basic_information(self):
		basic = OrderedDict()
		basic["name"] = self.name
		basic["start date"] = self.created.strftime("%H:%M %d-%m-%Y")
		basic["rank"] = self.rank
		basic["alliance"] = self.alliance
		basic["region"] = self.region
		
		return basic
	
	
	# return player possessions
	def possessions(self):	
		possessions = OrderedDict()
		#set currency
		
		possessions['damn'] = elements.models.convert_damn(self.damn)
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
		ranks = elements.models.Rank.objects.exclude(special=True)
		
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
	def perform_action(self, field, **kwargs):
		self.charactertimers.update_timer(field=field)
		
		if "times" in kwargs:
			times = kwargs['times']
		else:
			times = 1
			
		#add xp
		values = elements.models.GameBaseValues.objects.get(id=1)
		setattr(self, "xp", self.xp + getattr(values, field+"_xp") * times )
		self.save()
		
		#check if you ranked up
		self.check_rank()
	
	
	# create travel data
	def travel_stats(self):
		TravelInfo = namedtuple("TravelInfo", "region, cost_damn")
		regions = elements.models.Region.objects.exclude(name=self.region.name)
		travel_to = []
		
		for region in regions:
			cost = self.region.get_travel_cost(region, self)
			cost_damn = elements.models.convert_damn(cost)
			travel_to.append(TravelInfo(region=region.name, cost_damn=cost_damn))
		
		return travel_to
	
	
	
	#travel a character to a new region
	def travel(self, location):
		region = elements.models.Region.objects.get(name=location)
		cost = self.region.get_travel_cost(region, self)
		if self.damn < cost:
			flavor = "You don't have enough money to travel to %s." % region
			return flavor
		else:
			now = datetime.utcnow().replace(tzinfo=utc)
			travel_time = timedelta(seconds=self.transport.travel_timer)
			self.region = region
			self.charactertimers.travel = now + travel_time
			self.damn -= cost
			self.save()
			self.charactertimers.save()
			
			flavor = "Welcome in %s" % region
			return flavor
		
	
	#see if smuggle action succeeds
	def try_to_smuggle(self, smuggle):
		# increase counter for every try
		if smuggle == "booze":
			self.booze_tries += 1
		elif smuggle == "narcotics":
			self.narcotics_tries += 1
			
		self.save()
		
		values = elements.models.GameBaseValues.objects.get(id=1)
		rank_mod = getattr(values, smuggle + "_rank")
		tries_mod = getattr(values, smuggle + "_try") 
		
		#get chance to succeed
		tries = getattr(self, smuggle + "_tries")
		tries_chance = int(tries / tries_mod)
		tries_rank = int (rank_mod * self.rank.rank)
		chance = tries_chance + tries_rank		
		
		#see if player is succesfull
		roll = randint(0, 100)
		
		if roll < chance:
			return True
		
		# on fail you go to jail
		else:
			timer_min = getattr(values, smuggle + "_failed_min")
			timer_max = getattr(values, smuggle + "_failed_max")
			timer_random = getattr(values, smuggle + "_random")
			
			timer = elements.models.get_min_max_result(timer_min, timer_max, timer_random, self.rank.rank)
			timer_string = elements.models.convert_timedelta(timedelta(seconds=timer))
			flavor = "You got arrested and need to spend %s in jail" % timer_string
			inactive = "jail"
			self.charactertimers.update_timer(field="inactive", timer=timer, inactive=inactive)
			return elements.models.Result(category=inactive, flavor=flavor)
			
		
		
		
	
	
	
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
	narcotics = models.DateTimeField(default=now)					#every 30 minutes available for xp
	
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
		fields["narcotics"] = ""
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
						
			if field == "booze" or field == "narcotics":
				url = "contraband"
			elif field in group_crimes:
				url = "group crime"
			else:
				url = field
			
			#field.replace("_", " ")
			if now > timer:
				fields[field] = Link(url=url, timer="Now")
			else:
				fields[field] = Link(url=url, timer=elements.models.convert_timedelta(timer - now))
		
		return fields

			
	
	# get timer by field
	def check_timer(self, field, **kwargs):
		timer = getattr(self, field)
		now = datetime.utcnow().replace(tzinfo=utc)
		
		#check if in jail/hospital
		active = self.check_if_active()
		if active != True:
			return active
		
		if now > timer:
			return elements.models.Result(check=True, category="", flavor="Now")
		elif "contraband" not in kwargs:
			flavor = "You are still tired from your last %s. Please wait another %s before trying again." % (field.replace("_", " "), elements.models.convert_timedelta(timer - now))
			return elements.models.Result(check=False, category="tired", flavor=flavor)
		else:
			return elements.models.Result(check=True, category="", flavor="")



	def check_if_active(self):
		now = datetime.utcnow().replace(tzinfo=utc)
		
		if self.inactive < now:
			self.location=True
			self.save()
	
		elif self.location == False:
			flavor = "You are still locked up in jail for %s." % elements.models.convert_timedelta(self.inactive - now)
			return elements.models.Result(check=False, category="jail", flavor=flavor)
		elif self.location == None:
			flavor = "You are getting patched up in hospital. Please wait another %s." % elements.models.convert_timedelta(self.inactive - now)
			return elements.models.Result(check=False, category="hospital", flavor=flavor)
	
		return True
		
		
		
	
	
	#set a timer
	def update_timer(self, field, **kwargs):
		values = elements.models.GameBaseValues.objects.get(id=1)
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
		


class CharacterContraband(models.Model):
	""" keep track on characters contraband """
	
	character = models.OneToOneField(Character)
	
	beer = models.IntegerField(default=0)
	cider = models.IntegerField(default=0)
	cognaq = models.IntegerField(default=0)
	rum = models.IntegerField(default=0)
	vodka = models.IntegerField(default=0)
	whiskey = models.IntegerField(default=0)
	wine = models.IntegerField(default=0)
	
	cocaine = models.IntegerField(default=0)
	tabacco = models.IntegerField(default=0)
	morphine = models.IntegerField(default=0)
	glue = models.IntegerField(default=0)
	amfetamines = models.IntegerField(default=0)
	heroin = models.IntegerField(default=0)
	cannabis = models.IntegerField(default=0)
	
	def __unicode__(self):
		return "%s's contraband" % self.character
	
	
	#create object for character
	@staticmethod
	def create(character):
		character_contraband = CharacterContraband(
			character=character,
		)
		character_contraband.save()
	
	
	# get narcotics or booze items
	@staticmethod
	def get_booze_or_narcotics(smuggle):
		if smuggle == "booze":
			return ['beer', 'cider', 'cognaq', 'rum', 'vodka', 'whiskey', 'wine']
		elif smuggle == "narcotics":
			return ['cocaine', 'tabacco', 'morphine', 'glue', 'amfetamines', 'heroin', 'cannabis']
		else:
			print "bad input for contraband, use 'booze' or 'narcotics'"
			return
	
	
	
	#get maximum of booze or narcs on character
	def get_maximum(self, contraband):
		from_character = getattr(self.character.rank, contraband)
		from_transport = getattr(self.character.transport, contraband)
		total = from_character + from_transport
		return total
		
		
	#get current amount of booze or narcotics currently wielded
	def get_current(self, contraband):
		items = self.get_booze_or_narcotics(contraband)
		total = 0
		for item in items:
			total += getattr(self, item)
		
		return total
		
		
	# create the needed data for the booze/narcotics form
	def contraband_form(self, smuggle):
		Contraband = namedtuple("Contraband", "name price on_character")
		items = self.get_booze_or_narcotics(smuggle)
		inventory = []
	
		for item in items:
			name = item
			price = elements.models.convert_damn(getattr(self.character.region.regionprices, item))
			on_character = getattr(self, item)
			inventory.append(Contraband(name=name, price=price, on_character=on_character))
		
		return inventory	



class CharacterTransport(models.Model):
	""" regions player and there means of transport """
	
	character = models.ForeignKey(Character)
	region = models.ForeignKey('elements.Region')
	transport = models.ForeignKey('elements.Transport', null=True, blank=True)
	
	class Meta:
		unique_together = ("character", "region")
		
	def __unicode__(self):
		return "%s %s %s" % (self.character, self.region, self.transport)
		
	
	@staticmethod
	def create_transport(character):
		regions = elements.models.Region.objects.all()
		for region in regions:
			new_transport = CharacterTransport(
				character=character,
				region=region,
			)
			new_transport.save()
			
	
	## zou classmethod moeten zijn?
	#@staticmethod
	#def transport_overview(character):
		#chartransports = CharacterTransport.objects.filter(character=character).order_by('region__name')
		#overview = OrderedDict()
		
		#for chartransport in chartransports:
			#if chartransport.transport == None:
				#overview[chartransport.region.name] = "Available"
			#else:
				#overview[chartransport.region.name] = chartransport.transport.name
		
		#return overview
	


class CharacterCar(models.Model):
	""" cars a character owns plus the location they are in """
	
	character = models.ForeignKey(Character)
	
	car = models.ForeignKey('elements.Car')
	region = models.ForeignKey('elements.Region')
	hitpoints = models.IntegerField()
	safe = models.BooleanField(default=False)
	
	def __unicode__(self):
		return "%s: %s" % (self.character, self.car)
	
	# get car hp in percent
	def hp_percent(self):
		return int(self.hitpoints / (self.car.hitpoints / 100 + 0.0))



class CharacterGun(models.Model):
	""" cars a character owns plus the location they are in """
	
	character = models.ForeignKey(Character)
	
	gun = models.ForeignKey('elements.Gun')
	region = models.ForeignKey('elements.Region')
	safe = models.BooleanField(default=False)
	
	def __unicode__(self):
		return "%s: %s" % (self.character, self.gun)
		
		
		

class CharacterArmor(models.Model):
	""" cars a character owns plus the location they are in """
	
	character = models.ForeignKey(Character)
	
	armor = models.ForeignKey('elements.Armor')
	region = models.ForeignKey('elements.Region')
	
	def __unicode__(self):
		return "%s: %s" % (self.character, self.armor)
	


class CharacterHouse(models.Model):
	""" holds players house max 1 per region """
	
	character = models.ForeignKey(Character)
	region = models.ForeignKey('elements.Region')
	
	house = models.ForeignKey('elements.Housing', related_name="+", null=True)
	garage = models.ForeignKey('elements.Housing', related_name="+", null=True)
	basement = models.ForeignKey('elements.Housing', related_name="+", null=True)
	garden = models.ForeignKey('elements.Housing', related_name="+", null=True)
	
	class Meta:
		unique_together = ["character", "region"]
	
	
	def __unicode__(self):
		return "%s: %s house" % (self.character, self.region)
	
	
	#creates list to view house + rank in template
	def view_house(self):
		Part = namedtuple("Part", "name rank")
		subs = ['house', 'garage', 'basement', 'garden']
		show_house = []
		
		for sub in subs:
			field = getattr(self, sub)
			if field != None:
				show_house.append(Part(name=sub, rank=field.name))
		
		return show_house
	
	
	
	#show total (smuggle)space
	def total_storage(self):
		subs = ['house', 'garage', 'basement', 'garden']
		spaces = ['defense', 'booze', 'narcotics', 'cars']
		storage = OrderedDict()
		
		for sub in subs:
			field = getattr(self, sub)
			
			if field != None:
				for space in spaces:
					if space in storage:
						storage[space] += getattr(field, space)
					else:
						storage[space] = getattr(field, space)
			
		return storage
				
		
	
	
	
	
	


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
	
	region = models.ForeignKey('elements.Region')
	alliance = models.ForeignKey(Alliance, null=True)
	owner = models.ForeignKey(Character, null=True)
	
	def __unicode__(self):
		return self.name
