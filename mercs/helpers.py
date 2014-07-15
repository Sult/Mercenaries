from django.core.exceptions import FieldError
from importlib import import_module
from django.conf import settings

#sort a queryset by a object-method
#only works for methods that dont take extra arguments
def sort_queryset_by_method(queryset, method_string, reverse):
	unsorted_list = queryset.all()
	sorted_list = sorted(unsorted_list, key=lambda obj: getattr(obj, method_string)())
	if reverse:
		sorted_list.reverse()
	return sorted_list
	


#this method sorting also works for related field, bij giving the name of the related field:
#If the object and related field have the same fieldname, objects data will be taken
def sort_queryset_by_field(queryset, fieldname, reverse, **kwargs):
	if len(queryset) == 0:
		return queryset
	
	if "relation" not in kwargs:
		if reverse:
			fieldname = "-" + fieldname
		sorted_list = queryset.order_by(fieldname)
	else:
		name = ""
		try:
			if reverse:
				name = "-" + fieldname
			else:
				name = fieldname
			sorted_list = queryset.order_by(name)
			getattr(sorted_list[0], fieldname)
		except FieldError:
			name = kwargs["relation"] + "__" + fieldname
			if reverse:
				name = "-" + name
			sorted_list = queryset.order_by(name)
	
	return sorted_list
		


	
	

	
	
	
	
	
