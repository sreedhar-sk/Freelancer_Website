from django.db import models

# Create your models here.
class user_info(models.Model):
	user_name=models.CharField(max_length=50)
	email_id=models.CharField(max_length=50)
	password=models.CharField(max_length=10)

	def __str__(self):
		return user_name,password,email_id

class user_login_info(models.Model):
	user_info=models.ForeignKey(user_info, on_delete=models.CASCADE)
	user_name=models.CharField(max_length=50)
	password=models.CharField(max_length=10)

	def __str__(self):
		return user_name,password
