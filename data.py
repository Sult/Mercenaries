from elements.models import Rank, ShortJob, GameBaseValues, Region
from characters.models import Character
from django.contrib.auth.models import User


def add_ranks():
	all_ranks = (
		("Cadet", 1, 0, 49, 10, 1, 0),
		("Second Lieutenant", 2, 50, 99, 25, 2, 0),
		("Lieutenant", 3, 100, 199, 50, 4, 0),
		("Captain", 4, 200, 399, 100, 7, 0),
		("Major", 5, 400, 799, 250, 11, 1),
		("Lieutenant Colonel", 6, 800, 1599, 500, 16, 2),
		("Colonel", 7, 1600, 3199, 1000, 22, 4),
		("Brigadier", 8, 3200, 6399, 2000, 29, 7),
		("Major General", 9, 6400, 12799, 4000, 37, 11),
		("Lieutenant General", 10, 12800, 25599, 7000, 46, 16),
		("General", 11, 25600, 51199, 11000, 55, 22),
		("Marshall", 12, 51200, 102399, 16000, 65, 29),
		("Field Marshall", 13, 102400, 204799, 20000, 76, 37),
		("Military Attache", 13, 102400, 204799, 17500, 76, 37),				#\xc3 (e met streepje erop)  oplossen dat die er wel gebruikt kan worden
		("Mercenary Recruiter", 13, 102400, 204799, 17500, 76, 37),
	)
	
	for rank in all_ranks:
		new_rank = Rank(
			name = rank[0],
			rank = rank[1],
			min_xp = rank[2],
			max_xp = rank[3],
			hitpoints = rank[4],
			booze = rank[5],
			narcotics = rank[6],
		)
		new_rank.save()
		print new_rank
		
		



def add_regions():
	all_regions = (
		("Sulrod", 5, 	-5, 15, -10, 5, -15, 0, 10, 	10, 15, 5, -15, 0, -10, -5),
		("Hesor", 3, 	10, -5, 15, -10, 5, -15, 0,		-5, 0, -10, 5, -15, 10, 15),
		("Danraki", 5, 	0, 10, -5, 15, -10, 5, -15, 	15, -15, 10, -10, 5, -5, 0),
		("Inadyn", 3, 	-15, 0, 10, -5, 15, -10, 5,		0, 5, -5, 10, -10, 15, -15),
		("Bunasti", 5, 	5, -15, 0, 10, -5, 15, -10,		-15, -10, 15, -5, 10, 0, 5),
		("Adilton", 5, 	-10, 5, -15, 0, 10, -5, 15,		5, 10, 0, 15, -5, -15, -10),
		("Crest", 5, 	15, -10, 5, -15, 0, 10, -5,		-10, -5, -15, 0, 15, 5, 10),
	)
	
	for region in all_regions:
		new_region = Region(
			name = region[0],
			alliance_slots = region[1],
	
			beer = region[2],
			cider = region[3],
			cognaq = region[4],
			rum = region[5],
			vodka = region[6],
			whiskey = region[7],
			wine = region[8],
	
			cocaine = region[9],
			tabacco = region[10],
			morphine = region[11],
			glue = region[12],
			amfetamines = region[13],
			heroin = region[14],
			cannabis = region[15],
		)
		new_region.save()
		print new_region
	

def add_base_values():
	values = GameBaseValues(
		#All game timers (in seconds)
		##Normal actions
		travel = 5400,
		blood_buy = 3600,
		car_race = 1800,
		kill_attempt = 3600,
		bullet_deal = 3600,
		booze = 1800,
		drugs = 1800,
		##solo actions
		short_job = 90,
		medium_job = 300,
		long_job = 900,
		##group actions
		heist = 10800,
		organised_crime = 21600,
		raid = 43200,
		mega_oc = 86400,
		
			#action xp values
		short_job_xp = 1,
		medium_job_xp = 3,
		long_job_xp = 10,
		heist_xp = 90,
		organised_crime_xp = 180,
		raid_xp = 360,
		mega_oc_xp = 720,
		booze_xp = 1,
		drugs_xp = 3,
		
		#Booze base prices
		beer = 200,
		cider = 950,
		cognaq = 2500,
		rum = 2100,
		vodka = 1600,
		whiskey = 3100,
		wine = 450,
		#Drugs base values
		cocaine = 19000,
		tabacco = 800,
		morphine = 14000,
		glue = 300,
		amfetamines = 6600,
		heroin = 16000,
		cannabis = 4500,
	)
	values.save()



def add_short_jobs():
	some_jobs = (
		("Teach self defence to a group of children.", True, 10, 25, 500, 25, 30, 95, 35, False, 0, 0, 0),
		("Help the local police force maintain their guns.", True, 8, 50, 650, 30, 20, 92, 25, False, 0, 0, 0),
		("Clean the toilets in the barracks.", True, 7, 30, 900, 17, 15, 83, 65, False, 0, 0, 0),
		("Work as bouncer for a discotheek.", True, 7, 100, 1200, 20, 15, 88, 10, False, 0, 0, 0),
		("Work as bouncer in the harbor bar.", True, 4, 120, 1750, 30, 10, 85, 15, True, 15, 300, 25),
		("Pickpocket another mercenary.", False, 4, 0, 50000, 45, 2, 50, 50, True, 25, 420, 20),
		("Practice your acuracy with guns.", True, 0, 0, 0, 0, 2, 12, 25, False, 0, 0, 0),
		("Move furniture for a removal service.", True, 9, 50, 650, 20, 20, 95, 30, False, 0, 0, 0),
		("Steal lunchmoney from some school kids.", False, 10, 40, 650, 20, 25, 95, 15, False, 0, 0, 0),
		("Extort a local grocery store.", False, 8, 200, 1200, 10, 20, 92, 10, True, 25, 450, 40),
		("Blackmail the mahor with his affair", False, 5, 500, 4800, 30, 15, 79, 20, True, 30, 500, 30),
		("Pay an escort for oral sex.", False, 5, 55, 2000, 10, 20, 84, 25, True, 10, 250, 20),
	)
	
	for job in some_jobs:
		new_job = ShortJob(
			name=job[0],
			rarity=job[2],
			legal=job[1],
			damn_min=job[3],
			damn_max=job[4],
			damn_random=job[5],
			chance_min=job[6],
			chance_max=job[7],
			chance_random=job[8],
			timer=job[9],
			timer_min=job[10],
			timer_max=job[11],
			timer_random=job[12],
		)
		new_job.save()
		
		print new_job





add_ranks()
add_short_jobs()
add_regions()
add_base_values()



Character.create(User.objects.get(username="admin"))
