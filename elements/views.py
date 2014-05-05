from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.core.context_processors import csrf
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required

#convert model to dict for sessions
from django.forms.models import model_to_dict

from elements.models import ShortJob


@login_required
def short_job(request):
	character = request.user.character
	session = request.session
	timercheck = character.charactertimers.check_timer('short_job')
	
	
	#check if player is ready for job
	if timercheck.check:
		session['short_job_part'] = "form"
		if "short_job_list" not in request.session:
			session['short_job_list'] = ShortJob.get_job_list(character)
			
	else:
		session['short_job_timer'] = timercheck.timer
		session['short_job_part'] = "timer"
	
	#if action is taken
	if request.POST:
		session['short_job_part'] = "result"
		
		#update timer and xp
		character.perform_action("short_job")
		
		# check if succeeds and give consequences
		job = request.POST["short_job"]
		chance = session['short_job_list'][job]
		result = ShortJob.check_to_succeed(job, chance, character)
		
		
		#remove short_job_list and timer
		del session['short_job_list']
		
		return render(request, "shortjob.html", {"result": result})
		
	return render(request, "shortjob.html")




