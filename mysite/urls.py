"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

from firstpage.views import(
	home_screen_view,
)

from accounts.views import(
    registration_view,
    logout_view,
    login_view,
    account_view,
    email_change_view,
    user_profile_view,
    #user_edit_profile_view,
    must_authenticate_view,
) 



urlpatterns = [
    path('admin/', admin.site.urls),

    #Firstpage URLs
    path('', home_screen_view, name='home'),

    #Account URLs
    path('register/', registration_view, name='register'),
    path('logout/', logout_view, name='logout'),
    path('login/', login_view, name='login'),
    path('account/', account_view, name='account'),
    path('change_email/', email_change_view, name='change_email'),
    path('must_authenticte', must_authenticate_view, name='must_authenticate'),
    path('profile/', user_profile_view, name='profile'),
    #path('edit_profile/', user_edit_profile_view, name='edit_profile'),


    #Blog
    path('blog/', include('blog.urls', 'blog')),

    # Password reset links (ref: https://github.com/django/django/blob/master/django/contrib/auth/views.py)
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='registration/password_change_done.html'), 
    name='password_change_done'),
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='registration/password_change.html'), 
    name='password_change'),
    path('password_reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_done.html'),
    name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('reset/complete/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'),
    name='password_reset_complete'),
]


#when in developement mode,set 
if settings.DEBUG:
    urlpatterns+= static(settings.STATIC_URL, document_root= settings.STATIC_ROOT)
    urlpatterns+= static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)
