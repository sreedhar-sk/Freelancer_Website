from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


# Create your forms here.

class NewUserForm(UserCreationForm):
	email = forms.EmailField(required=True)
	Given_Name=forms.CharField(required=True)
	Surname=forms.CharField(required=False)

	class Meta:
		model = User
		fields = ("Given_Name","Surname", "email", "username","password1", "password2")

	def save(self, commit=True):
		user = super(NewUserForm, self).save(commit=False)
		user.email = self.cleaned_data['email']
		user.f_name = self.cleaned_data['Given_Name']
		user.l_name = self.cleaned_data['Surname']
		if commit:
			user.save()
		return user