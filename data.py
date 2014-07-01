from elements.models import Rank, GameBaseValues, Region, TravelMethod, Transport, Armor, Gun, Car
from elements.models import SinglePlayerJob, FailedSinglePlayerJob, RegionPrices, Housing
from characters.models import Character
from django.contrib.auth.models import User
from users.models import ExtendUser


def add_ranks():
	all_ranks = (
		("Cadet", 1, 0, 49, 200, 2, 0, False),
		("Second Lieutenant", 2, 50, 99, 375, 4, 0, False),
		("Lieutenant", 3, 100, 199, 725, 7, 0, False),
		("Captain", 4, 200, 399, 1250, 11, 1, False),
		("Major", 5, 400, 799, 1950, 16, 2, False),
		("Lieutenant Colonel", 6, 800, 1599, 2825, 22, 3, False),
		("Colonel", 7, 1600, 3199, 3875, 29, 5, False),
		("Brigadier", 8, 3200, 6399, 5100, 37, 7, False),
		("Major General", 9, 6400, 12799, 6500, 46, 9, False),
		("Lieutenant General", 10, 12800, 25599, 8075, 55, 12, False),
		("General", 11, 25600, 51199, 9825, 65, 16, False),
		("Marshall", 12, 51200, 102399, 11750, 75, 21, True),						#Capo rank
		("Field Marshall", 13, 102400, 204800, 14025, 85, 27, True),				# allaince leader
		("Military Attache", 12, 51200, 102399, 11750, 75, 21, True),				#\xc3 (e met streepje erop)  oplossen dat die er wel gebruikt kan worden// alliance diplomat
		("Mercenary Recruiter", 12, 51200, 102399, 11750, 75, 21, True),			# alliance recruiter
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
			special = rank[7],
		)
		new_rank.save()
		
		
		



def add_regions():
	all_regions = (
		("Sulrod", 5, 	0.95, 1.15, 0.9, 1.05, 0.85, 1, 1.10, 		1.10, 1.15, 1.05, 0.85, 1, 0.9, 0.95, 	10, 4),
		("Hesor", 3, 	1.10, 0.95, 1.15, 0.9, 1.05, 0.85, 1,		0.95, 1, 0.9, 1.05, 0.85, 1.10, 1.15, 	18, 2),
		("Danraki", 5, 	1, 1.10, 0.95, 1.15, 0.9, 1.05, 0.85, 		1.15, 0.85, 1.10, 0.9, 1.05, 0.95, 1, 	14, 10),
		("Inadyn", 3, 	0.85, 1, 1.10, 0.95, 1.15, 0.9, 1.05,		1, 1.05, 0.95, 1.10, 0.9, 1.15, 0.85, 	2, 16),
		("Bunasti", 5, 	1.05, 0.85, 1, 1.10, 0.95, 1.15, 0.9,		0.85, 0.9, 1.15, 0.95, 1.10, 1, 1.05, 	4, 20),
		("Adilton", 5, 	0.9, 1.05, 0.85, 1, 1.10, 0.95, 1.15,		1.05, 1.10, 1, 1.15, 0.95, 0.85, 0.9, 	20, 16),
		("Crest", 5, 	1.15, 0.9, 1.05, 0.85, 1, 1.10, 0.95,		0.9, 0.95, 0.85, 1, 1.15, 1.05, 1.10, 	26, 8),
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
			
			x = region[16],
			y = region[17],
		)
		new_region.save()
		
		region_prices = RegionPrices(
			region = new_region,
			
			beer = 0,
			cider = 0,
			cognaq = 0,
			rum = 0,
			vodka = 0,
			whiskey = 0,
			wine = 0,
	
			cocaine = 0,
			tabacco = 0,
			morphine = 0,
			glue = 0,
			amfetamines = 0,
			heroin = 0,
			cannabis = 0,
		)
		region_prices.save()

def add_base_values():
	values = GameBaseValues(
		#All game timers (in seconds)
		##Normal actions
		travel = 7200,
		blood_buy = 3600,
		car_race = 1800,
		kill_attempt = 3600,
		bullet_deal = 3600,
		booze = 1800,
		narcotics = 1800,
		##solo actions
		short_job = 10,					# 90 later
		medium_job = 10,				# 300 later
		long_job = 10,					# 3600 later
		##group actions
		heist = 10800,
		organised_crime = 21600,
		raid = 43200,
		mega_oc = 86400,
		
		#action xp values
		short_job_xp = 1,
		medium_job_xp = 3,
		long_job_xp = 30,
		heist_xp = 90,
		organised_crime_xp = 180,
		raid_xp = 360,
		mega_oc_xp = 720,
		booze_xp = 1,
		narcotics_xp = 3,
		
		#action fail chances 
		
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
		
		price_difference = 15,
		
		booze_min_chance=7,
		booze_max_chance=75,
		booze_try=30,										# every x gives 1% of extra chance
		booze_rank=2.5,										# times rank for base succes
		booze_failed_min=90,
		booze_failed_max=720,
		booze_random=10,
		
		narcotics_min_chance=6,
		narcotics_max_chance=65,
		narcotics_try=35,
		narcotics_rank=2,
		narcotics_failed_min=120,
		narcotics_failed_max=900,
		narcotics_random=10,
		
		
	)
	values.save()






def add_travel_methods():
	the_methods = (
		("Hitchhike", 7200, 0, "Hitchhike along with a caravan of the army.", 0, 0, 0, 0, 20),
		("Johnsen R8", 3600, 100000, "Army grade hummer that you can ride yourself.", 1, 0, 5, 1, 40),
		("Casta 4", 2700, 250000, "Small low powerd helicopter.", 2, 0, 10, 3, 70),
		("EC 391", 1800, 1000000, "Twin engine army helicopter.", 5, 1, 20, 6, 100),
		("PH-421 Transcopter", 1800, 2500000, "Fast heavyweigth transport helicopter", 10, 2, 30, 10, 140),
	)
	
	
	for method in the_methods:
		new_method = TravelMethod(
			name=method[0],
			travel_timer=method[1],
			price=method[2],
			description=method[3],
			guns=method[4],
			cars=method[5],
			booze=method[6],
			narcotics=method[7],
			travel_modifier=method[8],
		)
		new_method.save()
	

def add_transports():
	transports = (
		("Motor", 120, 100, 75000, 0),
		("Car", 110, 110, 150000, 30),
		("Armored Car", 100, 120, 300000, 60),
	)
	
	for transport in transports:
		new_transport = Transport(
			name=transport[0],
			attack=transport[1],
			defense=transport[2],
			price=transport[3],
			equip=transport[4],
		)
		new_transport.save()
	

def add_armors():
	armors = (
		("Z611 Bullet Proof Jacket", 15, Armor.TYPE_I, Armor.BAD, 4, 0, 20000),
		("Z615 Bullet Proof Jacket", 13, Armor.TYPE_I, Armor.NORMAL, 7, 0, 60000),
		("Z618 Bullet Proof Jacket", 10, Armor.TYPE_I, Armor.GOOD, 10, 10, 120000),
		
		("B3612 Bullet Proof Vest", 14, Armor.TYPE_IIA, Armor.BAD, 6, 10, 40000),
		("B7512 Bullet Proof Vest", 11, Armor.TYPE_IIA, Armor.NORMAL, 9, 10, 100000),
		("B9612 Bullet Proof Vest", 8, Armor.TYPE_IIA, Armor.GOOD, 12, 15, 160000),
		
		("Z611 Bullet Proof Jacket", 12, Armor.TYPE_II, Armor.BAD, 8, 15, 80000),
		("Z615 Bullet Proof Jacket", 9, Armor.TYPE_II, Armor.NORMAL, 11, 15, 140000),
		("Z618 Bullet Proof Jacket", 6, Armor.TYPE_II, Armor.GOOD, 14, 20, 200000),
		
		("H6451 Bullet Proof Vest", 10, Armor.TYPE_IIIA, Armor.BAD, 10, 20, 120000),
		("H8373 Bullet Proof Vest", 7, Armor.TYPE_IIIA, Armor.NORMAL, 13, 20, 180000),
		("H9622 Bullet Proof Vest", 4, Armor.TYPE_IIIA, Armor.GOOD, 16, 30, 240000),
		
		("G52 Bullet Proof Jacket", 8, Armor.TYPE_III, Armor.BAD, 12, 30, 160000),
		("G74 Bullet Proof Jacket", 5, Armor.TYPE_III, Armor.NORMAL, 15, 30, 220000),
		("G81 Bullet Proof Jacket", 2, Armor.TYPE_III, Armor.GOOD, 18, 45, 280000),
		
		("S473 Body Armor", 6, Armor.TYPE_IV, Armor.BAD, 14, 45, 200000),
		("S571 Body Armor", 3, Armor.TYPE_IV, Armor.NORMAL, 17, 45, 260000),
		("S669 Body Armor", 1, Armor.TYPE_IV, Armor.GOOD, 20, 60, 300000),
	)
	
	for armor in armors:
		new_armor = Armor(
			name=armor[0],
			rarity=armor[1],
			category=armor[2],
			quality=armor[3],
			defense=armor[4],
			equip=armor[5],
			price=armor[6],
		)
		new_armor.save()



def add_guns():
	the_guns = (
		("Rhodes T19", 6, Gun.PISTOL, 0.75, 19, 2, 1150),
		("Nelson B780", 7, Gun.PISTOL, 0.75, 10, 4, 1400),
		("47 Warren B", 5, Gun.PISTOL, 0.8, 12, 4, 1850),
		("Parker P", 8, Gun.PISTOL, 0.8, 15, 4, 2450),
		("Rhodes B4", 4, Gun.PISTOL, 0.9, 15, 5, 4900),
		("Foster Tara 7", 1, Gun.PISTOL, 0.9, 13, 7, 3350),
		("Parker PII", 3, Gun.PISTOL, 1, 8, 7, 4750),
		("Burton 17", 2, Gun.PISTOL, 1, 12, 8, 5600),
		
		("Rhodes M14", 5, Gun.MACHINE_PISTOL, 0.15, 20, 4, 5000),
		("71 Warren M", 8, Gun.MACHINE_PISTOL, 0.22, 48, 4, 6950),
		("Schwartz 46p", 4, Gun.MACHINE_PISTOL, 0.15, 31, 5, 7880),
		("Schwartz 48p", 6, Gun.MACHINE_PISTOL, 0.2, 42, 6, 12450),
		("Foster Tara M7", 7, Gun.MACHINE_PISTOL, 0.1, 42, 8, 13500),
		("Freeman 4", 1, Gun.MACHINE_PISTOL, 0.35, 28, 7, 15250),
		("Maurer 31-1", 2, Gun.MACHINE_PISTOL, 0.35, 50, 5, 17500),
		("Schwartz 41i", 3, Gun.MACHINE_PISTOL, 0.9, 35, 3, 16000),
		
		("Schwartz 17", 3, Gun.SHOTGUN, 0.85, 8, 12, 2800),
		("4SG Conger", 6, Gun.SHOTGUN, 0.2, 6, 14, 4900),
		("Schwartz 4b", 5, Gun.SHOTGUN, 0.7, 4, 19, 7400),
		("Warren SGa", 2, Gun.SHOTGUN, 0.3, 12, 18, 11050),
		("Big Parker 22", 7, Gun.SHOTGUN, 0.95, 2, 22, 8590),
		("Tuck 407", 4, Gun.SHOTGUN, 0.25, 5, 24, 5650),
		("Firebreath IV", 8, Gun.SHOTGUN, 0.7, 5, 16, 12000),
		("Tuck 908", 1, Gun.SHOTGUN, 0.95, 4, 25, 6600),
		
		("Keller PTa", 3, Gun.ASSAULT_RIFLE, 0.6, 30, 4, 22350),
		("78B Conger", 4, Gun.ASSAULT_RIFLE, 0.5, 44, 3, 24500),
		("Nelson AR 14", 7, Gun.ASSAULT_RIFLE, 0.2, 52, 3, 20300),
		("Knox DD", 5, Gun.ASSAULT_RIFLE, 0.15, 43, 7, 16450),
		("Freeman X7-1", 6, Gun.ASSAULT_RIFLE, 0.23, 60, 4, 12840),
		("Maurer 7a", 2, Gun.ASSAULT_RIFLE, 0.22, 48, 8, 6990),
		("Freeman Y4-1", 8, Gun.ASSAULT_RIFLE, 0.05, 50, 6, 10500),
		("Keller PT", 1, Gun.ASSAULT_RIFLE, 0.65, 36, 4, 14780),
		
		("Big Parker Q", 4, Gun.SNIPER_RIFLE, 2, 1, 32, 16500),
		("R74 Burton", 3, Gun.SNIPER_RIFLE, 1, 1, 24, 18450),
		("R84 Burton", 2, Gun.SNIPER_RIFLE, 1.85, 1, 44, 4590),
		("Knox 4-1a", 5, Gun.SNIPER_RIFLE, 0.1, 30, 15, 6580),
		("Nelson BT7a", 6, Gun.SNIPER_RIFLE, 0.6, 5, 17, 12980),
		("Walsh Prober", 7, Gun.SNIPER_RIFLE, 0.1, 5, 28, 17350),
		("Walsh Prober 74", 8, Gun.SNIPER_RIFLE, 0.3, 8, 16, 14600),
		("Harwood TT", 1, Gun.SNIPER_RIFLE, 0.26, 15, 24, 16090),
	)
	
	for gun in the_guns:
		new_gun = Gun(
			name = gun[0],
			rarity = gun[1],
			category = gun[2],
			accuracy = gun[3],
			magazine = gun[4],
			damage = gun[5],
			price = gun[6],
		)
		new_gun.save()



def add_cars():
	some_cars = (
		("Thornton 74 Racing", Car.SPORTSCAR, 1, 311, 1, 1, 100, 120000),
		("Hines 450-XR", Car.SPORTSCAR, 2, 228, 2, 2, 200, 86000),
		("Thornton Big Lagoon", Car.SPORTSCAR, 4, 241, 2, 4, 250, 64000),
		("4T Downs", Car.SPORTSCAR, 6, 239, 2, 4, 300, 22000),
		("Howard Sapphire 1", Car.SPORTSCAR, 7, 259, 2, 4, 400, 13000),
		("Wilburn Kinder", Car.SPORTSCAR, 3, 255, 2, 2, 350, 32000),
		("Shirlene", Car.SPORTSCAR, 5, 281, 1, 1, 250, 26000),
		("Spleener X-408", Car.SPORTSCAR, 8, 284, 2, 2, 200, 25000),
		
		("Tuckr 73 Shaft", Car.TRUCK, 3,	110,	3,	9,	20000,	30000),
		("Negation TR", Car.TRUCK, 5,	90,	4,	10,	25000,	16000),
		("Titan 4", Car.TRUCK, 6,	128,	3,	7,	18500,	18000),
		("Galvin RR Tire", Car.TRUCK, 4,	121,	2,	6,	12000,	39000),
		("Tuckr Raptoid", Car.TRUCK, 1, 104,	2,	6,	10000,	45000),
		("Hertha	Truck", Car.TRUCK, 7, 114,	2,	8,	13500,	26000),
		("Xener Mckenzie", Car.TRUCK, 8,	120,	2,	8,	16000,	29000),
		("Titan 6", Car.TRUCK, 2, 142,	2,	8,	14000,	34000),
	
		("Negation TR-Mini",	Car.PICKUP,	3,	162,	2,	6,	2000,	4200),
		("Junk 89B",	Car.PICKUP,	5,	140,	2,	6,	2600,	4600),
		("Dayton Fife",	Car.PICKUP,	2,	132,	3,	7,	2900,5900),
		("Xener Outbound",	Car.PICKUP,	4,155,	3,	7,	3300,	2300),
		("Xener Outback",	Car.PICKUP,	6,	144,2,	6,	3800,	4700),
		("Marrero Red",	Car.PICKUP,	7,188,2,	6,	2200,	3500),
		("Little Foot",	Car.PICKUP,1,163,	2,	6,	3000,	9400),
		("Galvin TR Insert",	Car.PICKUP,	8,	158,	2,	6,	4000,	7800),
	
		("Hines Overtone",	Car.CAR,	7,	220,	2,	4,	500,	9100),
		("Tarver 4",	Car.CAR,	6,	235,	4,	4,	600,	8800),
		("Wilburn T402",	Car.CAR,	5,	194,	3,	4,	750,	7200),
		("Dayton Pia",	Car.CAR,	8,	175,	3,	4,	950,	6800),
		("Hester Cardwell",	Car.CAR,	4,	224,	4,	4,	1100,	6600),
		("Wilburn T406",	Car.CAR,	1,	166,	4,	4,	1800,	11200),
		("Hester Nowlin",	Car.CAR,	2,	190,	4,	6,	1650,	9400),
		("Hines Benz 4",	Car.CAR,	3,	132,	4,	6,	2000,	7800),
							
		("Tarver 6",	Car.JEEP,	1,	142,	4,	8,	12000,	16000),
		("Junk 408",	Car.JEEP,	5,	163,4,	8,	10000,	14800),
		("Marrero Blue",	Car.JEEP,	6,	192,	4,	6,	11000,	12600),
		("Xener Cherist",	Car.JEEP,	4,	158,	4,	6,	13500,	8900),
		("Garnett 3-T",	Car.JEEP,	7,	159,	2,	6,	9500,	11000),
		("Humsy Beat",	Car.JEEP,	3,	149,2,	6,	8000,	13600),
		("Humsy 840-6",	Car.JEEP,	8,	156,	3,	5,	7000,	9800),
		("Marrero Gold",	Car.JEEP,	2,	181,	2,	6,	6000,	16500),
	)
	
	for car in some_cars:
		new_car = Car(
			name=car[0],
			category=car[1],
			rarity=car[2],
			speed=car[3],
			seats=car[4],
			max_seats=car[5],
			hitpoints=car[6],
			price=car[7],
		)
		new_car.save()





add_ranks()
add_regions()
add_base_values()
add_travel_methods()
add_transports()
add_armors()
add_guns()
add_cars()


user = User.objects.get(username="admin")
Character.create(user, name="Marmotte")
new = ExtendUser(
	user=user,
)
new.save()




def add_single_player_jobs():
	#add short jobs
	the_type = SinglePlayerJob.SHORT

	the_jobs = (
		("Teach self defence to a group of children.", the_type, True, 10, 25, 500, 25, 30, 95, 35),
		("Help the local police force maintain their guns.", the_type, True, 8, 50, 650, 30, 20, 92, 25),
		("Clean the toilets in the barracks.", the_type, True, 7, 30, 900, 17, 15, 83, 65),
		("Work as bouncer for a discotheek.", the_type, True, 7, 100, 1200, 20, 15, 88, 10),
		("Work as bouncer in the harbor bar.", the_type, True, 4, 120, 1750, 30, 10, 85, 15),
		("Pickpocket another mercenary.", the_type, False, 4, 0, 50000, 45, 2, 50, 50),
		("Practice your acuracy with guns.", the_type, True, 0, 0, 0, 0, 4, 15, 25),
		("Move furniture for a removal service.", the_type, True, 9, 50, 650, 20, 20, 95, 30),
		("Steal lunchmoney from some school kids.", the_type, False, 10, 40, 650, 20, 25, 95, 15),
		("Extort a local grocery store.", the_type, False, 8, 200, 1200, 10, 20, 92, 10),
		("Blackmail the mahor with his affair", the_type, False, 5, 500, 4800, 30, 15, 79, 20),	
		("Pay an escort for oral sex.", the_type, False, 5, 55, 2000, 10, 20, 84, 25),
	)
	
	for job in the_jobs:
		new_job = SinglePlayerJob(
			flavor = job[0],
			category = job[1],
			#legal = job[2],
			rarity = job[3],			
	
			car = False,
			gun = False,
			damn = True,
		
			chance_min = job[7],
			chance_max = job[8],
			chance_random = job[9],
	
			damn_min = job[4],
			damn_max = job[5],
			damn_random = job[6],
		)
		new_job.save()
		
	
	# medium jobs
	the_jobs = (
		("Work as security at a bank.",	True, 9, False, False, True, 20,	70,	35, 250,	2500,	25),
		("Help the casino 'deal' with some problems.",	False, 9, False, False, True, 20,	75,	25,400,	3100,	25),
		("Test your luck in a scratch cards.",	True, 7, True, False, False, 10,	45,	15,0, 0, 0),
		("Steal a car from the corner of the street.",	False, 6, True, False, False, 10,	50,	20,0, 0, 0),
		("Ambush and hijack a car at a country road.",	False, 5, True, False, False, 10,	55,25,0, 0, 0),
		("Contest in the regional skeet shooting.",	True, 7, False, True, False, 10,	45,	15,0, 0, 0),
		("Steal from the gun depot of local police station.",	False, 6, False, True, False, 10,	50, 20,0, 0, 0),
		("Hit a gangster on the head and steal his gun.",	False, 5, False, True, False, 10,	58,	25,0, 0, 0),
		("Stand guard at the royal palace.",	True, 4, False, False, True, 12,	80,	30,400,	3200,	30),
		("Work as bodyguard for a national celebrity.",	True, 3, False, False, True, 10,	75,	20,800,	3300,	30),
		("Fight in an underground fighting club.",	False, 4, False, False, True, 15,	75,	35,1000,	2900,	40),
		("Rob a drugdealer on the street.",	False, 2, True, True, True, 10,	45,	50, 0,	15000,	50),
		("Pay a prostitute to help you out with your needs.",	False, 5, False, False, True, 15,	70,	25, 200, 4000,	10),
		("Steal gun from another mercanary.",	False, 2, False, True, False, 10,	50,	50,0, 0, 0),
		("Steal a car from another mercenary.",	False, 2, True, False, False, 10,	50, 50,0, 0, 0),
		("Work as a repo man for a big firm.",	True, 4, False, False, True, 5,	70,	25,500,	3500,	20),
	)
	
	for job in the_jobs:
		new_job = SinglePlayerJob(
			flavor = job[0],
			category = SinglePlayerJob.MEDIUM,
			#legal = job[1],
			rarity = job[2],	
	
			car=job[3],
			gun=job[4],
			damn=job[5],
	
			chance_min=job[6],
			chance_max=job[7],
			chance_random=job[8],
	
			damn_min=job[9],
			damn_max=job[10],
			damn_random=job[11],
	
		)
		new_job.save()
	
	

def add_short_failures():
	some_failures = (
		("Teach self defence to a group of children.", "You could not find the address.", 6, False, 0, 0, 0, True),
		("Teach self defence to a group of children.", "After you accidently kicked a kid in the face, they sent you home without being paid.", 5, False, 0, 0, 0, True),
		("Teach self defence to a group of children.", "You hurt your wrist and had to go to hospital for TIMER.", 4, True, 30, 180, 30, True),
		
		("Help the local police force maintain their guns.", "After dropping a gun for the second time, you where asked to leave.", 5, False, 0, 0, 0, True),
		("Help the local police force maintain their guns.", "You ended up in a furious discussion about teaspoons after trying to help. You ran out and went home.", 3, False, 0, 0, 0, True),
		("Help the local police force maintain their guns.", "While reloading a gun you managed to shoot yourself in the leg, resulting in a TIMER checkup in hospital.", 3, True, 60, 200, 20, True), 
		
		("Clean the toilets in the barracks.", "Disgusted by the big piles of feces you refused the job.", 6, False, 0, 0, 0, True),
		("Clean the toilets in the barracks.", "After puking for an hour, you deceided to call it a day and take your losses.", 4, False, 0, 0, 0, True),
		("Clean the toilets in the barracks.", "You got a itching rash all over your body and had to go to hospital to get checked out. taking you a TIMER.", 2, True, 40, 210, 35, True),
		
		("Work as bouncer for a discotheek.", "Someone else took the job before you.", 6, False, 0, 0, 0, True),
		("Work as bouncer for a discotheek.", "You got drunk at work and got sent home.", 5, False, 0, 0, 0, True),
		("Work as bouncer for a discotheek.", "You had to get yourself checked in hospital for TIMER after you got into a fight with a colleague.", 3, True, 30, 190, 25, True),
		
		("Work as bouncer in the harbor bar.", "You are in hospital for TIMER. A customer pulled a knife at you which resulted in you needing some stitches.", 3, True, 60, 240, 25, True),
		("Work as bouncer in the harbor bar.", "You where flirting all the time and let in some douches. Job failed", 4, False, 0, 0, 0, True),
		("Work as bouncer in the harbor bar.", "You got into a fight with some sailors about a girl. putting you in hospital for TIMER", 4, True, 60, 190, 20, True),
		
		("Pickpocket another mercenary.", "After noticing the target was twice as big as you, you deceided to leave.", 3, False, 0, 0, 0, False),
		("Pickpocket another mercenary.", "The cops caught you and sent you to jail for TIMER.", 5, True, 30, 180, 40, False),
		("Pickpocket another mercenary.", "This was the last drop for the cops. you had already some outstanding tickets and deceided to drop you in jail for TIMER.", 2, True, 60, 300, 10, False),
		
		("Move furniture for a removal service.", "After you figured out your travelcost wouldn't be refunded you walked away.", 4, False, 0, 0, 0, True),
		("Move furniture for a removal service.", "Figuring out you would be working with your arch enemy, you walked away.", 4, False, 0, 0, 0, True),
		
		("Steal lunchmoney from some school kids.", "After a kid told the principal, it didn't take long for the cops to show up. They put you in jail for TIMER.", 5, True, 45, 170, 20, False),
		("Steal lunchmoney from some school kids.", "The schoolbully stood up to you and you had to run away.", 2, False, 0, 0, 0, False),
		("Steal lunchmoney from some school kids.", "After getting into a moral dilemma, you went home empty handed.", 3, False, 0, 0, 0, False),
		
		("Extort a local grocery store.", "You noticed this store was already under maffia control and deceided not to try it.", 6, False, 0, 0, 0, False),
		("Extort a local grocery store.", "The shop owner went to the police and you got caught adn now you need to spend TIMER in jail.", 2, True, 35, 190, 20, False),
		("Extort a local grocery store.", "You didn't notice the cop in the store and you got busted immediately. You are now in jail for TIMER.", 2, True, 50, 210, 5, False), 
		
		("Blackmail the mahor with his affair", "Turned out his wife already knew and now you stand empty handed.", 6, False, 0, 0, 0, False),
		("Blackmail the mahor with his affair", "The mahor turned to the cops and you got busted. You are now spending TIMER in jail.", 4, True, 50, 220, 15, False),
	)
	
	for failure in some_failures:
		new_failure = FailedSinglePlayerJob(
			job = SinglePlayerJob.objects.get(flavor=failure[0]),
			flavor = failure[1],
			rarity = failure[2],
			legal = failure[7],
	
			timer = failure[3],
			timer_min = failure[4],
			timer_max = failure[5],
			timer_random = failure[6],
		)
		new_failure.save()
		
	


def add_medium_failures():
	some_failures = (
		("Work as security at a bank.", "You showed up at the wrong bank.", True, 4, False, 0, 0, 0),
		("Work as security at a bank.", "They saw you tried to take some money and you got kicked out.", True, 3, False, 0, 0, 0),
		("Work as security at a bank.", "They saw you tried to take some money and called the cops. You need to spend TIMER in jail now.", False, 3, True, 190, 610, 15),
		
		("Help the casino 'deal' with some problems.", "You get sent home after they deceided you wheren't fit enough for the job.", True, 6, False, 0, 0, 0),
		("Help the casino 'deal' with some problems.", "Once you started 'extracting' some information, cops showed up and put you in jail for TIMER.", False, 2, True, 220, 630, 15),
		("Help the casino 'deal' with some problems.", "You got your ass kicked by the target leaving you on a hospital trip for TIMER.", True, 2, True, 160, 420, 20),
		
		("Test your luck in a scratch cards.", "You forgot to bring your wallet.", True, 6, False, 0, 0, 0),
		("Test your luck in a scratch cards.", "The ticket you found was so damaged it couldnt be accepted anymore.", True, 2, False, 0, 0, 0),
		("Test your luck in a scratch cards.", "You got distracted and forgot what you where about to do.", True, 2, False, 0, 0, 0),
		
		("Steal a car from the corner of the street.", "You could not find a suitable car.", True, 4, False, 0, 0, 0),
		("Steal a car from the corner of the street.", "The cops caught you in the act and put you in jail for TIMER.", False, 1, True, 320, 590, 20),
		("Steal a car from the corner of the street.", "You cut yourself kicking in the window and you are TIMER in hospital.", True, 2, True, 160, 500, 20),
		
		("Ambush and hijack a car at a country road.", "After a long chase, the wrecked the car and the cops busted you. Now you spend TIMER in jail.", False, 2, True, 320, 550, 20),
		("Ambush and hijack a car at a country road.", "You are TIMER in hospital after the driver kicked your theeth out.", True, 3, True, 120, 540, 30),
		("Ambush and hijack a car at a country road.", "After 3 hours you still didn't find a target and went home.", True, 7, False, 0, 0, 0),
		
		("Contest in the regional skeet shooting.", "A hard gust of wind blew the target way off and you missed putting you out of competition.", True, 3, False, 0, 0, 0),
		("Contest in the regional skeet shooting.", "You forgot to load your gun and missed your most needed shot.", True, 3, False, 0, 0, 0),
		("Contest in the regional skeet shooting.", "You accidently shot yourself in the foot. you got rushed to hospital and need to spend TIMER there.", True, 3, True, 190, 420, 20),
		
		("Steal from the gun depot of local police station.", "After seeing more then four cops busy polishing their weapons. you deceided to turn around.", True, 4, False, 0, 0, 0),
		("Steal from the gun depot of local police station.", "You got caught and are now forced to stay where you are for TIMER.", False, 2, True, 210, 600, 20),
		
		("Hit a gangster on the head and steal his gun.", "He pulled a shotgun on you and should be lucky you are still alive.", True, 4, False, 0, 0, 0),
		("Hit a gangster on the head and steal his gun.", "You got back even harder and need to get some stitches. Costing you TIMER in hospital.", True, 3, True, 200, 400, 15),
		
		("Stand guard at the royal palace.", "You fell asleep and got discharged.", True, 5, False, 0, 0, 0),
		("Stand guard at the royal palace.", "You accidently cut yourself with the bajonet of the gun. You are now in hospital for TIMER.", True, 3, True, 180, 420, 25),
		
		("Work as bodyguard for a national celebrity.", "After you kept flirting with the celebrity you got sent home.", True, 5, False, 0, 0, 0),
		("Work as bodyguard for a national celebrity.", "You got into a fight with another bodygaurd, resulting in you needing a trip to hospital, taking a full TIMER.", True, 3, True, 180, 590, 20),
		
		("Fight in an underground fighting club.", "You won, but got disqualified by faul play.", True, 6, False, 0, 0, 0),
		("Fight in an underground fighting club.", "You got knocked K.O. and had to be brought to hospital, taking TIMER.", True, 2, True, 210, 500, 15),
		("Fight in an underground fighting club.", "Cops raided the place and putting everyone in jail for TIMER.", False, 2, True, 200, 400, 10),
		
		("Rob a drugdealer on the street.", "You got stabbed in the chest. You spent now TIMER in hospital.", True, 2, True, 180, 580, 20),
		("Rob a drugdealer on the street.", "After a short fight, cops busted you both and put you in jail for TIMER.", False, 2, True, 280, 700, 20),
		
		("Steal gun from another mercanary.", "When you spotted a target, it was surrounded by lots of friends and you had to call it a day.", True, 5, False, 0, 0, 0),
		("Steal gun from another mercanary.", "The target got upset and gave you a good kidney punch. You are now in hospital for TIMER.", True, 2, True, 180, 600, 20),
		("Steal gun from another mercanary.", "He called the cops on you and you are TIMER in jail.", False, 2, True, 180, 600, 20),
		
		("Steal a car from another mercenary.", "Your target managed to scare you away.", True, 5, False, 0, 0, 0),
		("Steal a car from another mercenary.", "He drove of fast, dragging you with it. When you finaly broke free you where all bruised up and had to go to hospital for TIMER.", True, 2, True, 180, 600, 20),
		("Steal a car from another mercenary.", "Cops spotted you right after you drove of. Busted you and put you in jail for TIMER.", False, 2, True, 0, 0, 0),
		
		("Work as a repo man for a big firm.", "You lost your goods, so they kept your paycheck.", True, 4, False, 0, 0, 0),
		("Work as a repo man for a big firm.", "After the door got opened by a huge guy, you deceided to turn around.", True, 4, False, 0, 0, 0),
	)
	
	for failure in some_failures:
		new_failure = FailedSinglePlayerJob(
			job = SinglePlayerJob.objects.get(flavor=failure[0]),
			flavor = failure[1],
			legal = failure[2],
			rarity = failure[3],
	
			timer = failure[4],
			timer_min = failure[5],
			timer_max = failure[6],
			timer_random = failure[7],
		)
		new_failure.save()


		
add_single_player_jobs()
add_short_failures()
add_medium_failures()
		



def add_houses():
	the_houses = (
		#House
		("Building Lot", Housing.HOUSE, 0, 40000, 0, 0, 0, 0, "Surveyed and bounded plot of land that is set aside for constructing a building."),
		("Bungalow", Housing.HOUSE, 1, 50000, 5, 10, 0, 0, "Small house with only a single story and a nice varanda."),
		("House", Housing.HOUSE, 2, 100000, 10, 25, 0, 0, "Reasonable sized house of two stories with room for more."),
		("Villa", Housing.HOUSE, 3, 500000, 20, 45, 0, 0, "Large and luxurious country house in its own grounds."),
		("Mansion", Housing.HOUSE, 4, 500000, 30, 75, 0, 0, "Large and impressive house. It won't get better than this."), 
		
		#garages
		("Workplace", Housing.GARAGE, 1, 20000, 0, 15, 0, 0, "Separate room for some DIY."),
		("Garage", Housing.GARAGE, 2, 50000, 0, 55, 0, 1, "Indoor space to park a car."),
		("Garage Box", Housing.GARAGE, 3, 10000, 0, 115, 0, 2, "Expand the garage to hold another car."),
		("Helipad", Housing.GARAGE, 4, 500000, 0, 115, 0, 2, "Helicopter landing platform.\n(Reduces travel time from this region by 5 minutes.)"),
		
		#basements
		("Walk in Basement", Housing.BASEMENT, 1, 20000, 0, 0, 5, 0, "Small basement to keep some supplies."),
		("Basement", Housing.BASEMENT, 2, 50000, 0, 0, 15, 0, "Underground room for storage."),
		("Cellar", Housing.BASEMENT, 3, 100000, 0, 0, 35, 0, "Set of underground rooms."),
		("Bunker", Housing.BASEMENT, 4, 1500000, 20, 0, 35, 0, "Extremely strengthened underground hiding room.\n(Only one time possible.)"), 
		
		#gardens
		("Garden", Housing.GARDEN, 1, 20000, 0, 0, 5, 0, "Area of ground where flowers and plants grow."),
		("Shed", Housing.GARDEN, 2, 50000, 0, 0, 15, 0, "A small barn. A little hut meant for storing in the backyard."),
		("Pond", Housing.GARDEN, 3, 100000, 0, 0, 35, 0, "Small type of lake. Dug by men to decorate the garden."),
		("Dock Terrace", Housing.GARDEN, 4, 500000, 0, 0, 35, 0, "Jetty near the water where a small boat could be docked.\n(This building gives acces to the 'Smuggle' group crime."),
	)
	
	
	for house in the_houses:
		new_house = Housing(
			name=house[0],
			description=house[8],
			category=house[1],
			rank=house[2],
			price=house[3],
			defense=house[4],
			booze=house[5],
			narcotics=house[6],
			cars=house[7],
		)
		new_house.save()
		

add_houses()
		
