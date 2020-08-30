from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from accounts.models import Account, UserProfile

from accounts.forms import (RegistrationForm, AccountAuthenticationForm,
							 AccountUpdateForm, EmailUpdateForm, UpdateUserProfileForm
							)

from blog.models import BlogPost



# Create your views here.
def registration_view(request):
	context = {}

	user = request.user
	#First check if user is already logged in.
	if user.is_authenticated:
		return redirect('home')

	if request.POST:
		form = RegistrationForm(request.POST)
		if form.is_valid():
			form.save()
			email = form.cleaned_data.get('email')
			raw_password = form.cleaned_data.get('password1')
			account = authenticate(email=email, password= raw_password)
			login(request, account)
			return redirect('home')
		else:
			context['registration_form'] = form
	else: #GET request
		form = RegistrationForm()
		context['registration_form'] = form
	return render(request, 'accounts/register.html', context)



def logout_view(request):
	logout(request)
	return redirect('home')



def login_view(request):
	context = {}

	user = request.user
	#First check if user is already logged in.
	if user.is_authenticated:
		return redirect('home')

	#If user try to Login..
	if request.POST:
		form = AccountAuthenticationForm(request.POST)
		if form.is_valid():
			email = request.POST['email']
			password = request.POST['password']
			user =authenticate(email=email, password=password)

			#if Login and account exist, then login user..
			if user:
				login(request, user)
				return redirect('home')

	else:
		form = AccountAuthenticationForm()

	context['login_form'] = form
	return render(request, 'accounts/login.html', context)



# Account changes,
def account_view(request):

	if not request.user.is_authenticated:
		return redirect('login')

	context = {}

	if request.POST:
		form = AccountUpdateForm(request.POST, instance=request.user)
		if form.is_valid():
			form.initial = {
				"email": request.POST['email'],
				"username": request.POST['username'],
			}
			form.save()
			context['prompt_user_success'] = "Succesfully Updated"
	else:
		form = AccountUpdateForm(
			initial={
				"email": request.user.email,
				"username": request.user.username,
			}
		)
	context['account_form'] = form
	return render(request, 'accounts/account.html', context)



def email_change_view(request):

	if not request.user.is_authenticated:
		return redirect('login')	

	context = {}

	if request.POST:
		form = EmailUpdateForm(request.POST, instance=request.user)
		if form.is_valid():
			form.initial = {
				"email": request.POST['email'],
			}
			form.save()
			context['prompt_success'] = "Changes made"
	else:
		form = EmailUpdateForm(
			initial={
				"email": request.user.email,
			}
		)
	context['email_form'] = form
	return render(request, 'accounts/change_email.html')



#User profile
def user_profile_view(request):
	context = {}

	user = request.user
	if not user.is_authenticated:
		return redirect('must_authenticate')

	#IF user is Authenticated, will be abel to edit profile
	user_profile = request.user.userprofile
	if request.POST:
		form = UpdateUserProfileForm(request.POST or None, request.FILES or None, instance=user_profile)
		if form.is_valid():
			obj = form.save(commit=False)
			obj.save()
			context['prompt_success'] = "Succesfully Updated"
			user_profile = obj
	
	form = UpdateUserProfileForm(
			initial = {
				"description": user_profile.description,
				"level": user_profile.level,
				"age": user_profile.age,
				"gender": user_profile.gender,
				"programme": user_profile.programme,
				"phone": user_profile.phone,
				"profile_pic": user_profile.profile_pic,
			}
		)
	context['form'] = form

	#Show Blog that belongs to the author in profile page,
	blog_posts = BlogPost.objects.filter(author=request.user)
	context['blog_posts'] = blog_posts
	
	return render(request,"accounts/profile.html", context)



#user edit profile
#def user_edit_profile_view(request):
#	context = {}
#	user = request.user
#	if not user.is_authenticated:
#		return redirect('must_authenticate')

	#IF user is Authenticated, will be abel to edit profile
#	user_profile = request.user.userprofile
#	if request.POST:
#		form = UpdateUserProfileForm(request.POST or None, request.FILES or None, instance=user_profile)
#		if form.is_valid():
#			obj = form.save(commit=False)
#			obj.save()
#			context['prompt_success'] = "Succesfully Updated"
#			user_profile = obj
	
#	form = UpdateUserProfileForm(
#			initial = {
#				"description": user_profile.description,
#				"level": user_profile.level,
#				"age": user_profile.age,
#				"gender": user_profile.gender,
#				"programme": user_profile.programme,
#				"phone": user_profile.phone,
#				"profile_pic": user_profile.profile_pic,
#			}
#		)

#	context['form'] = form
#	return render(request,"accounts/edit_profile.html", context)



#User Authenticate..
def must_authenticate_view(request):
	context = {}
	return render(request, 'accounts/must_authenticate.html',context)