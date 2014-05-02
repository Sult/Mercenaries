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
	
	if "short_job_list" not in request.session:
		request.session['short_job_list'] = ShortJob.get_job_list(request.user.character)
	
	if request.POST:
		#update timer and xp
		request.user.character.perform_action("short_job")
		
		# check if succeeds and give consequences
		job = request.POST["short_job"]
		chance = request.session['short_job_list'][request.POST["short_job"]]
		request.user.character.check_to_succeed(job, chance)
		
		#remove short_job_list
		del request.session['short_job_list']
		
				
		return HttpResponseRedirect(reverse('short job'))
	
	return render(request, "shortjob.html")
