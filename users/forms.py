from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from django.core.exceptions import ObjectDoesNotExist

from characters.models import Character


class RegistrationForm(UserCreationForm):
	"""
	edit the User Registration form to add an emailfield
	"""
	
	email = forms.EmailField(required=True)
	
	class Meta:
		model = User
		fields = ('username', 'email', 'password1', 'password2')
	
	def save(self, commit=True):
		user = super(RegistrationForm, self).save(commit=False)
		user.email = self.cleaned_data['email']
		
		if commit:
			user.save()
		return user
	
	def __init__(self, *args, **kwargs):
		super(RegistrationForm, self).__init__( *args, **kwargs)

		#for fieldname in ['username', 'password1', 'password2']:
			#self.fields[fieldname].help_text = None




class LoginForm(forms.Form):
	"""create login form with placeholders for fields"""

	username = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Username:'}))
	password = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'placeholder': 'Password:'}))

	def clean(self):
		username = self.cleaned_data.get('username')
		password = self.cleaned_data.get('password')
		user = authenticate(username=username, password=password)
		if not user or not user.is_active:
			raise forms.ValidationError("Login invalid")
		return self.cleaned_data

	def login(self, request):
		username = self.cleaned_data.get('username')
		password = self.cleaned_data.get('password')
		user = authenticate(username=username, password=password)
		return user
		


# choose a charactername
class CharacterNameForm(forms.Form):
	name = forms.CharField(required=True, widget=forms.TextInput(attrs={'placeholder': 'Charactername:'}))


	def clean_name(self):
		name = self.cleaned_data['name']
		name.capitalize()
		try:
			character = Character.objects.get(name=name)
			raise forms.ValidationError("There is already a user with that name!")
		except ObjectDoesNotExist:
			pass
		
		return name
		
