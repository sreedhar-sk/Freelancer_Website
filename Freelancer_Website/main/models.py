from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

class service_provider_info(models.Model):
	user_provider=models.OneToOneField(User,related_name="user_provider",on_delete=models.CASCADE,blank=True,null=True)
	users_wishlist=models.ManyToManyField(User,related_name="users_wishlist",blank=True)
	users_cart=models.ManyToManyField(User,related_name="users_cart",blank=True)
	profile_pic=models.ImageField(null=True,blank=True)
	first_name=models.CharField(max_length=50)
	last_name=models.CharField(max_length=50)
	email=models.EmailField(max_length=50)
	mobile_num=models.BigIntegerField(null=True)
	ratings=models.PositiveIntegerField(null=True)
	service=models.CharField(max_length=300,null=True)
	skills=models.CharField(max_length=300,null=True)
	location=models.CharField(max_length=300,null=True)
	hourly_rate=models.FloatField(null=True)
	description=models.CharField(max_length=500,null=True)

	class Meta:
		db_table="provider"

class ticket_info(models.Model):
	task_type=models.CharField(max_length=300)  
	user_stories=models.CharField(max_length=1000)
	service=models.CharField(max_length=300)
	tools=models.CharField(max_length=500)
	time_frame=models.CharField(max_length=300)
	location=models.CharField(max_length=300,null=True)
	hourly_rate=models.FloatField(null=True)
	class Meta:
		db_table="ticket"
