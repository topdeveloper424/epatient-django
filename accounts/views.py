from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.hashers import make_password,check_password
from accounts.models import User
from .forms import SingupForm
from .models import User
from twilio.rest import Client
from django.conf import settings
from django.http import JsonResponse
from django.http import HttpResponse
from django.core.mail import send_mail

import random
from datetime import datetime
import json
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
# Create your views here.

def signin(request):
    if request.method == "GET":
        return render(request,'auth/login.html')
    else:
        if request.session.test_cookie_worked():
            request.session.delete_test_cookie()

        try:
            User.objects.get(useremail = request.POST['useremail'])
        except User.DoesNotExist:
            return render(request,'auth/login.html',{'message':'you are not a user !'})
        user = User.objects.get(useremail = request.POST['useremail'])
        if user.user_type == 'AD':
            if request.POST['password'] == user.password:
                if user.is_active == 0:
                    request.session['temp_email'] = request.POST['useremail']
                    return redirect('accounts:verify_phone')
                else:
                    request.session['useremail'] = request.POST['useremail']
                    request.session['phone_number'] = user.phone_number
                    request.session['user_type'] = user.user_type
                    return redirect('main:dashboard')

        matchcheck = check_password(request.POST['password'],user.password)
        print(request.POST['password'])
        if matchcheck:
            if user.is_active == 0:
                request.session['temp_email'] = request.POST['useremail']
                return redirect('accounts:verify_phone')
            else:
                request.session['useremail'] = request.POST['useremail']
                request.session['phone_number'] = user.phone_number
                request.session['user_type'] = user.user_type
                return redirect('main:dashboard')
        return render(request,'auth/login.html',{'message':'Password is not matched with user email !'})
def signup(request):
    if request.method == "GET":
        form = SingupForm()
        return render(request,'auth/register.html',{'form':form})
    else:
        form = SingupForm(request.POST)
        if request.POST['password'] != request.POST['confrm_password']:
            return render(request,'auth/register.html',{'form':form,'confirm_error':'confirm password does not match'})
        if form.is_valid():
            signup_item = form.save(commit=False)
            signup_item.password = make_password(signup_item.password)
            signup_item.verify_code = random.randint(1000,9999)
            signup_item.save()
            request.session['temp_email'] = signup_item.useremail
            return redirect('accounts:verify_phone')
        return render(request,'auth/register.html',{'form':form})

def signout(request):
    try:
        del request.session['useremail']
    except KeyError:
        pass
    try:
        del request.session['phone_number']
    except KeyError:
        pass
    try:
        del request.session['user_type']
    except KeyError:
        pass
    return redirect('main:index')
    
def verify_phone(request):
    try:
        email = request.session['temp_email']
        user = User.objects.get(useremail=email)
#        message = client.messages \
#                .create(
#                     body="E-Patient verify code. \n" + user.verify_code ,
#                     from_=settings.SMS_FROM_PHONE,
#                     to=user.phone_number
#                 )

        return render(request,'auth/verify.html',{'phone_number':user.phone_number})
    except Exception:
        pass
    return redirect('accounts:sign_up')
def verify(request):
    print(request.GET['code'])
    email = request.session['temp_email']
    user = User.objects.get(useremail=email)
    signup_time = user.verify_time
    send_time = signup_time.replace(tzinfo=None)
    datetime_now = datetime.now()
    diff = datetime_now - send_time
    elapsed_ms = diff.total_seconds()
    print(str(elapsed_ms))

    response_data = {}

    if request.GET['code']!= user.verify_code:
        response_data['status'] = "incorrect"
        return HttpResponse(json.dumps(response_data),content_type="application/json")
    elif elapsed_ms > settings.VERIFY_TIME:
        response_data['status'] = "timeout"
        return HttpResponse(json.dumps(response_data),content_type="application/json")
    else:
        user.is_active = 1
        user.save()
        request.session['useremail'] = user.useremail
        request.session['phone_number'] = user.phone_number
        request.session['user_type'] = user.user_type
        response_data['status'] = "success"
        return HttpResponse(json.dumps(response_data),content_type="application/json")
    return render(request)

def resend_code(request):
    mode = request.GET['mode']
    response_data = {}
    try:
        email = request.session['temp_email']
        user = User.objects.get(useremail=email)
        code = random.randint(1000,9999)
        user.verify_code = code
        user.save()
        if mode == 1:
            msg = MIMEMultipart('alternative')
            msg['Subject'] = "Epatient"
            msg['From'] = settings.FROM_EMAIL
            msg['To'] = email
            html = "<html><head></head><body><div>this is your verify code :&nbsp; </div><h3>"+str(user.verify_code)+"</h3></body></html>"
            part = MIMEText(html, 'html')
            msg.attach(part)
            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.ehlo()
            server.login(settings.FROM_EMAIL, settings.EMAIL_PASSWORD)

            server.sendmail(settings.FROM_EMAIL,email, msg.as_string())
            server.quit()

#        message = client.messages \
#                .create(
#                     body="E-Patient verify code. \n" + code ,
#                     from_=settings.SMS_FROM_PHONE,
#                     to=user.phone_number
#                 )
        response_data['status'] = 'sent'
        return HttpResponse(json.dumps(response_data),content_type="application/json")
    except Exception:
        pass
    response_data['status'] = 'error'
    return HttpResponse(json.dumps(response_data),content_type="application/json")

def verify_email(request):
    try:
        email = request.session['temp_email']
        user = User.objects.get(useremail=email)

        msg = MIMEMultipart('alternative')
        msg['Subject'] = "Epatient"
        msg['From'] = settings.FROM_EMAIL
        msg['To'] = email
        html = "<html><head></head><body><div>this is your verify code : &nbsp; </div><h3>"+str(user.verify_code)+"</h3></body></html>"
        part = MIMEText(html, 'html')
        msg.attach(part)
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(settings.FROM_EMAIL, settings.EMAIL_PASSWORD)

        server.sendmail(settings.FROM_EMAIL,email, msg.as_string())
        server.quit()


        return render(request,'auth/verify_email.html',{'useremail':email})
    except Exception:
        pass
    return redirect('accounts:sign_up')
