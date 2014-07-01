from django_cron import CronJobBase, Schedule
from elements.models import Region, GameBaseValues, RegionPrices

from random import randint

class SetContrabandPrices(CronJobBase):
	#test
	RUN_EVERY_MINS = 5
	RETRY_AFTER_FAILURE_MINS = 1
	schedule = Schedule(run_every_mins=RUN_EVERY_MINS, retry_after_failure_mins=RETRY_AFTER_FAILURE_MINS)
	
	#for real
	#RUN_AT_TIMES = ["00:00", "00:30", "1:00", "1:30", "2:00", "2:30", "3:00", "3:30", "4:00", "4:30", "5:00", "5:30", 
	#				"6:00", "6:30", "7:00", "7:30", "8:00", "8:30", "9:00", "9:30", "10:00", "10:30", "11:00", "11:30", 
	#				"12:00", "12:30", "13:00", "13:30", "14:00", "14:30", "15:00", "15:30", "16:00", "16:30",  "17:00", "17:30", 
	#				"18:00", "18:30", "19:00", "19:30", "20:00", "20:30", "21:00", "21:30",  "22:00", "22:30", "23:00", "23:30"]
	
	#schedule = Schedule(run_at_times=RUN_AT_TIMES)
	
	code = "elements.setcontrabandprices"
	
	def do(self):
		regions = Region.objects.all()
		#contraband = ['cocaine', 'tabacco', 'morphine', 'glue', 'amfetamines', 'heroin', 'cannabis',
		#				'beer', 'cider', 'cognaq', 'rum', 'vodka', 'whiskey', 'wine']
		contraband = RegionPrices._meta.get_all_field_names()
		contraband.remove('id')
		contraband.remove('region')
		
		values = GameBaseValues.objects.get(id=1)
		
		for region in regions:
			for field in contraband:
				basic = getattr(values, field)
				factor = getattr(region, field)
				minimum = int(basic * factor * (100 - values.price_difference + 0.0) / 100)
				maximum = int(basic * factor * (100 + values.price_difference + 0.0) / 100)
				price = randint(minimum, maximum)
				
				region_price = RegionPrices.objects.get(region=region)
				setattr(region_price, field, price)
				region_price.save()
