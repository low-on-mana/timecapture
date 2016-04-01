from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import TimeUser

@receiver(post_save,sender=TimeUser)
def send_email_to_user_after_creation(sender,**kwargs):
	return 4/0
