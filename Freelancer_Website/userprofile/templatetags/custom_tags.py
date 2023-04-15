from django import template
from django.contrib.auth.models import User

register = template.Library()

@register.filter(name='get_username')

def get_username(sender_id):
    sender = User.objects.get(id=sender_id)
    return sender.username
