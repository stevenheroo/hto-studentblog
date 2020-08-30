from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate

from accounts.models import Account
from accounts.models import UserProfile


class RegistrationForm(UserCreationForm):
	email = forms.EmailField(max_length=60, help_text='Required. Type a valid email')

	class Meta:
		model = Account
		fields = ("email", "username", "firstname", "lastname", "password1", "password2")




#Login Authentication form, 
class AccountAuthenticationForm(forms.ModelForm):
	#specifying a password field widget... so it won't make password visible 		
	password = forms.CharField(label='password', widget=forms.PasswordInput)

	class Meta:
		model = Account
		fields = ('email', 'password')

	#Checks for errors, user details are valid
	def clean(self):
		if self.is_valid():
			email = self.cleaned_data['email']
			password = self.cleaned_data['password']
			if not authenticate(email=email, password=password):
				raise forms.ValidationError("Invalid Email or Password. Try Again")
				
		


#Account Update form,
class AccountUpdateForm(forms.ModelForm):

	class Meta:
		model = Account
		fields = ('email', 'username')


	def clean_email(self):
		if self.is_valid():
			email = self.cleaned_data['email']
			try:
				#checking if account exits,so if
				account = Account.objects.exclude(pk=self.instance.pk).get(email=email)
			except Account.DoesNotExist:
				return email
			raise forms.ValidationError('Email "%s" is already in use.' % account.email)


	def clean_username(self):
		if self.is_valid():
			username = self.cleaned_data['username']
			try:
				#checking if username exits,if so
				account = Account.objects.exclude(pk=self.instance.pk).get(username=username)
			except Account.DoesNotExist:
				return username
			raise forms.ValidationError('Username "%s" is already in use.' % account.username)



#Email Update form,
class EmailUpdateForm(forms.ModelForm):

	class Meta:
		model = Account
		fields = ('email',)


	def clean_email(self):
		if self.is_valid():
			email = self.cleaned_data['email']
			try:
				#checking if email exits,so if
				account = Account.objects.exclude(pk=self.instance.pk).get(email=email)
			except Account.DoesNotExist:
				return email
			raise forms.ValidationError('Email "%s" is already in use.' % account.email)




#class UserProfileForm(forms.ModelForm):
#
#	class Meta:
#		model = UserProfile
#		fields = '__all__'
#		exclude = ['user','profile_pic']
#
#		widgets = {
#			'age': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
#			'level': forms.Select(attrs={'class': 'form-control'}),
#			'gender': forms.Select(attrs={'class': 'form-control'})
#		}



class UpdateUserProfileForm(forms.ModelForm):

	class Meta:
		model = UserProfile
		fields = '__all__'
		exclude = ['user','profile_pics']

		widgets = {
			'age': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
			'level': forms.Select(attrs={'class': 'form-control'}),
			'gender': forms.Select(attrs={'class': 'form-control',})
		}

	def save(self, commit=True):
		user_profile = self.instance
		user_profile.description = self.cleaned_data['description']
		user_profile.level = self.cleaned_data['level']
		user_profile.age = self.cleaned_data['age']
		user_profile.programme = self.cleaned_data['programme']
		user_profile.gender = self.cleaned_data['gender']
		user_profile.phone = self.cleaned_data['phone']


		if self.cleaned_data['profile_pic']:
			user_profile.profile_pic = self.cleaned_data['profile_pic']


		if commit:
			user_profile.save()
		return user_profile


#Image ProfileChange
#class ChangeProfilePicture(forms.ModelForm):
#
#	class Meta:
#		model = UserProfile
#		fields = ["profile_pic"]
#
#
#	def save(self, commit=True):
#		user_profile_pic = self.instance
#		user_profile_pic.profile_pic = self.cleaned_data['profile_pic']

#		if commit:
#			user_profile_pic.save()
#		return user_profile
