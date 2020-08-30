from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

from django.conf import settings


# Create your models here.

class MyAccountManager(BaseUserManager):
	def create_user(self, email, username, firstname, lastname, password=None):
		#Raise flag
		if not email:
			raise ValueError("Users must have an email address")
		if not username:
			raise ValueError("Users must have a username")
		if not firstname:
			raise ValueError("Users must have a firstname")
		if not lastname:
			raise ValueError("Users must have a lastname")
		
		

		#If no flag raised,create
		user  = self.model(
				email =self.normalize_email(email),
				username = username,	
				firstname = firstname,
				lastname = lastname,	
			)
		user.set_password(password)
		user.save(using=self._db)
		return user


	def create_superuser(self, email, username, firstname, lastname, password):
		user = self.create_user(
				email =self.normalize_email(email),
				password = password,
				username = username,
				firstname = firstname,
				lastname = lastname, 	
			)
		user.is_admin = True
		user.is_staff = True
		user.is_superuser = True
		user.save(using=self._db)
		return user

		
class Account(AbstractBaseUser):
	email					= models.EmailField(verbose_name="email", max_length=60, unique=True)
	username				= models.CharField(max_length=30, unique=True)
	firstname				= models.CharField(verbose_name= 'first name', max_length=30, default='')
	lastname				= models.CharField(verbose_name= 'last name', max_length=30, default='')
	date_joined				= models.DateTimeField(verbose_name='date joined', auto_now_add=True)
	last_login				= models.DateTimeField(verbose_name='last login', auto_now=True)
	is_admin				= models.BooleanField(default=False)
	is_active				= models.BooleanField(default=True)
	is_staff				= models.BooleanField(default=False)
	is_superuser			= models.BooleanField(default=False)

	#Login Field , Required field for registering
	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['username','firstname','lastname']

	#Reference  
	objects = MyAccountManager()


	def __str__(self):
		return self.email

	#For checking permissions. to keep it simple all admin have ALL permissons
	def has_perm(self, perm, obj=None):
		return self.is_admin

	# Does this user have permission to view this app? (ALWAYS YES FOR SIMPLICITY)
	def has_module_perms(self, app_label):
		return True



#define primary location for image files... 
def upload_location1(instance, filename, **kwargs):
	file_path = 'userprofile/{user_id}/{filename}'.format(
			user_id=str(instance.user.id), filename=filename
		)
	return file_path

SEX = [
	("M" , "MALE"),
	("F" , "FEMALE"),
]

LEVEL = [
	("100" , "HUNDRED"),
	("200" , "TWO HUNDRED"),
	("300" , "THREE HUNDRED"),
	("400" , "FOUR HUNDRED"),
]



class UserProfile(models.Model):
	user					= models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	description				= models.CharField(max_length=500, blank=True)
	level					= models.CharField(max_length=10, blank=True, choices=LEVEL)
	gender					= models.CharField(max_length=1, blank=True, choices=SEX)
	programme				= models.CharField(max_length=50, blank=True)
	phone					= models.CharField(max_length=30, blank=True)
	profile_pic				= models.ImageField(upload_to=upload_location1, blank=True)
	age 					= models.DateField(verbose_name='Birth date', blank=True, null=True)
	friends					= models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='friends', blank=True)
	created_on				= models.DateTimeField(auto_now_add=True, verbose_name='created on')
	udated_on				= models.DateTimeField(auto_now=True, verbose_name='updated on')

	def __str__(self):
		return self.user.username

	def get_friends(self):
		return self.friends.all()

	def get_count_friends(self):
		return self.friends.all().count()


