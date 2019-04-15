"""Epatient URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path,include
from . import views

app_name = 'accounts'

urlpatterns = [
    path('sign-in', views.signin,name='sign_in'),
    path('sign-up', views.signup,name='sign_up'),
    path('sign-out', views.signout,name='sign_out'),
    path('verify-phone', views.verify_phone,name='verify_phone'),
    path('verify', views.verify,name='verify'),
    path('resend-code', views.resend_code,name='resend_code'),
    path('verify-email', views.verify_email,name='verify_email'),

]
