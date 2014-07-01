from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist


def still_alive(function):
	def wrap(request, *args, **kwargs):
		try:
			request.user.character_set.get(alive=True)
			return function(request, *args, **kwargs)
		except ObjectDoesNotExist:
			return HttpResponseRedirect(reverse('create character'))

	return wrap
