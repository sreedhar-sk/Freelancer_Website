from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User
from main.models import *
class ProvideServiceForm(ModelForm):
	class Meta:
		model=service_provider_info
		fields = ("first_name","last_name","email","mobile_num","service","skills","location","hourly_rate","description")
		labels = {
			"first_name": "What is your First Name?",
			"last_name": "What is your Last Name?",
			"email": "What is your Email Address?",
			"mobile_num": "What is your Mobile Number?",
			"service": "What are the services you provide?",
			"skills": "What are your top skills?",
			"location": "In which country do you live?",
			"hourly_rate": "What is your preffered rate per hour?",
			"description":"Say About You (Something Special..!!)",
		}
		widgets={
			"first_name": forms.TextInput(attrs={'class':'form-control'}),
			"last_name": forms.TextInput(attrs={'class':'form-control'}),
			"email": forms.EmailInput(attrs={'class':'form-control'}),
			"mobile_num": forms.TextInput(attrs={'class':'form-control'}),
			"service": forms.TextInput(attrs={'class':'form-control'}),
			"skills": forms.TextInput(attrs={'class':'form-control'}),
			"location": forms.TextInput(attrs={'class':'form-control'}),
			"hourly_rate": forms.TextInput(attrs={'class':'form-control'}),
			"description":forms.Textarea(attrs={'class':'form-control','cols': 102, 'rows': 20}),
		}


class ticketform(ModelForm):
	class Meta:
		model=ticket_info
		fields = ("task_type","user_stories","service","tools","time_frame","location","hourly_rate")
		labels = {
			"task_type": "Describe the task type?",
			"user_stories": "What is the Requirement? (Mention as User Stories)",
			"service": "What is the type of application category to develop?",
			"tools": "Mention the technology, framework, packages and libraries to be used (if specific)?",
			"time_frame": "What is the expected Time Frame and Delivery Deployment Time?",
			"location": "What is your preffered Location?",
			"hourly_rate": "What is your preffered rate per hour?",
		}
		widgets={
			"task_type": forms.TextInput(attrs={'class':'form-control'}),
			"user_stories": forms.Textarea(attrs={'class':'form-control','cols': 102, 'rows': 20}),
			"service": forms.EmailInput(attrs={'class':'form-control'}),
			"tools": forms.Textarea(attrs={'class':'form-control','cols': 102, 'rows': 20}),
			"time_frame": forms.TextInput(attrs={'class':'form-control'}),
			"location": forms.TextInput(attrs={'class':'form-control'}),
			"hourly_rate": forms.TextInput(attrs={'class':'form-control'}),
		}


class EditForm(UserChangeForm):
    def __init__(self, *args, **kwargs):
        super(EditForm, self).__init__(*args, **kwargs)
        del self.fields['password']

    class Meta:
        model = User
        fields = ('username','email','first_name','last_name')

        widgets={
			"username": forms.TextInput(attrs={'class':'form-control'}),
			"email": forms.EmailInput(attrs={'class':'form-control'}),
			"first_name": forms.TextInput(attrs={'class':'form-control'}),
			"last_name": forms.TextInput(attrs={'class':'form-control'}),
		}