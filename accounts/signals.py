from django.db.models.signals import post_save, post_delete
from django.conf import settings
from django.dispatch import receiver

from .models import UserProfile



#If user deletes Profile then also delete image from db. 
@receiver(post_delete, sender=UserProfile)
def submission_delete(sender, instance, **kwargs):
	instance.profile_pic.delete(False)


#Checks if profile is Unique and has a unique username.
def post_save_user_profile_reciever(sender, **kwargs):
	if kwargs['created']:
		user_profile = UserProfile.objects.create(user=kwargs['instance'])
post_save.connect(post_save_user_profile_reciever, sender=settings.AUTH_USER_MODEL)



