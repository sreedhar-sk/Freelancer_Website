from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.utils import timezone

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
	users_ticket=models.ForeignKey(User,related_name="users_ticket",on_delete=models.CASCADE,blank=True,null=True)
	task_type=models.CharField(max_length=300)  
	user_stories=models.CharField(max_length=1000)
	service=models.CharField(max_length=300)
	tools=models.CharField(max_length=500)
	time_frame=models.CharField(max_length=300)
	location=models.CharField(max_length=300,null=True)
	hourly_rate=models.FloatField(null=True)
	class Meta:
		db_table="ticket"

class Audit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=100)
    timestamp = models.DateTimeField(default=timezone.now)
    details = models.TextField(blank=True, null=True)
    timestamp_local = models.DateTimeField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.action} ({self.timestamp_local})"

    def save(self, *args, **kwargs):
        if not self.timestamp_local:
            self.timestamp_local = timezone.localtime(self.timestamp)
        super().save(*args, **kwargs)

class Chat(models.Model):
    sender = models.PositiveIntegerField()
    recipient = models.PositiveIntegerField()
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)