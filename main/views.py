from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core import serializers
from django.contrib.auth.hashers import make_password

from accounts.models import User
from main.models import Appointment,Problem,Medication, Test
from django.db.models import Q
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import json


def index(request):
    return render(request, 'index.html')

def view_profile(request):
    useremail = request.session['useremail']
    user = User.objects.filter(useremail = useremail)
    if user:
        serialized_queryset = serializers.serialize('json', user)
        return HttpResponse(json.dumps(serialized_queryset),content_type="application/json")
    return HttpResponse(json.dumps(""),content_type="application/json")



def dashboard(request):
    user = User.objects.get(useremail = request.session['useremail'])
    request.session['username'] = user.first_name + " "+ user.last_name
    if user.user_type == 'PA':
        return render(request, 'main/patient/dashboard.html')
    elif user.user_type == 'MD':
        return render(request, 'main/medical/dashboard.html')
    elif user.user_type == 'AD':
        return render(request, 'main/admin/dashboard.html')

#get incoming appointments for this week
def incoming_appoint(request):
    time_threshold = datetime.now()+timedelta(days=6)
    useremail = request.session['useremail']
    user = User.objects.get(useremail = useremail)
    accept_appoints = Appointment.objects.filter(user_id = user.id).filter(status='A').filter(limit_date__gt = datetime.now()).filter(limit_date__lt=time_threshold)
    if len(accept_appoints) > 0:
        serialized_queryset = serializers.serialize('json', accept_appoints)
        return HttpResponse(json.dumps(serialized_queryset),content_type="application/json")
    return HttpResponse(json.dumps(""),content_type="application/json")

def book(request):
    return render(request,'main/patient/book.html')

#search available doctors for selected period
def searchDoctors(request):
    pick_date = request.GET['date']
    b_date = datetime.strptime(pick_date,'%Y-%m-%d')
    fromString = request.GET['from']
    toString = request.GET['to']
    fromArray = fromString.split('-')
    toArray = toString.split('-')
    fromHour = 0
    toHour = 0
    if fromArray[1] == 'PM':
        fromHour = 12 + int(fromArray[0])
    else:
        fromHour = int(fromArray[0])
    if toArray[1] == 'PM':
        toHour = 12 + int(toArray[0])
    else:
        toHour = int(toArray[0])
    begin = datetime.strptime(str(fromHour)+":"+fromArray[2], '%H:%M').time()
    end = datetime.strptime(str(toHour)+":"+toArray[2], '%H:%M').time()
    doctors = Appointment.objects.filter(status='A').filter(Q(book_date=b_date))
    doctors1 = doctors.filter(Q(from_time__lt=begin)).filter(Q(to_time__gt=begin))
    doctors2 = doctors.filter(Q(from_time__lt=end)).filter(Q(to_time__gt=end))

    users = User.objects.filter(is_active=True).filter(user_type ='MD')
    av_doctors = []
    for user in users:
        flag = 0
        for doctor in doctors1:
            if user.id == doctor.doctor_id:
                flag = 1
        for doctor in doctors2:
            if user.id == doctor.doctor_id:
                flag = 1
        if flag == 0:
            av_doctors.append(user)
    serialized_queryset = serializers.serialize('json', av_doctors)
    return HttpResponse(json.dumps(serialized_queryset),content_type="application/json")

#create one book(appointment)        
def create_book(request):
    response = {}
    try:
        doctor_pk = request.GET['pk']
        book_text = request.GET['book_text']
        pick_date = request.GET['date']
        b_date = datetime.strptime(pick_date,'%Y-%m-%d')
        fromString = request.GET['from']
        toString = request.GET['to']
        fromArray = fromString.split('-')
        toArray = toString.split('-')
        fromHour = 0
        toHour = 0
        if fromArray[1] == 'PM':
            fromHour = 12 + int(fromArray[0])
        else:
            fromHour = int(fromArray[0])
        if toArray[1] == 'PM':
            toHour = 12 + int(toArray[0])
        else:
            toHour = int(toArray[0])
        begin = datetime.strptime(str(fromHour)+":"+fromArray[2], '%H:%M').time()
        end = datetime.strptime(str(toHour)+":"+toArray[2], '%H:%M').time()
        end_date = datetime.strptime(pick_date+"-"+str(fromHour)+":"+fromArray[2],'%Y-%m-%d-%H:%M')
        print(end_date)

        user = User.objects.get(useremail = request.session['useremail'])
        appoint = Appointment(user_id = user.id,doctor_id=doctor_pk,book_date=pick_date,from_time=begin,to_time = end,book_text=book_text,limit_date=end_date)
        appoint.save()
        response['status'] = "success"
    except Exception:
        response['status'] = "error"
    return HttpResponse(json.dumps(response),content_type="application/json")


# get accepted, pending, expired, rejected appointments for 6 days from now
def view_book(request):
    time_threshold = datetime.now()-timedelta(days=6)
    accept_appoints = Appointment.objects.filter(status='A').filter(limit_date__gt=time_threshold)
    pending_appoints = Appointment.objects.filter(status='P').filter(limit_date__gt=time_threshold)
    reject_appoints = Appointment.objects.filter(status='R').filter(limit_date__gt=time_threshold)
    
#    time = datetime.strptime(datetime.datetime.today().strftime('%H:%M'))
    real_pending_appoints = pending_appoints.filter(limit_date__gte = datetime.now())
    expired_appoints = pending_appoints.filter(limit_date__lt=datetime.now())

    print(accept_appoints)
    print(real_pending_appoints)
    print(expired_appoints)
    print(reject_appoints)

    return render(request,"main/patient/view_book.html",{'accepted':accept_appoints,'pending':real_pending_appoints,'rejected':reject_appoints,'expired':expired_appoints})

#get details for selected appointment
def appoint_detail(request):
    try:
        appoint = Appointment.objects.get(id=request.GET['pk'])
        doctor_id = appoint.doctor_id
        doctor = User.objects.get(id = doctor_id)

        response = {}
        response['doctor'] = doctor.first_name + " " + doctor.last_name
        response['pub_date'] = appoint.pub_date.strftime('%Y-%m-%d %H:%M')
        response['text'] = appoint.book_text
    except Exception:
        response['doctor'] = 'error'
    return HttpResponse(json.dumps(response),content_type="application/json")

#change appointment text for selected appointment
def change_appoint(request):
    try:
        response = {}
        appoint = Appointment.objects.get(id=request.GET['pk'])
        appoint.book_text = request.GET['book_text']
        appoint.save()
        response['status'] = 'success'
    except Exception:
        response['status'] = 'error'
    return HttpResponse(json.dumps(response),content_type="application/json")

#cnacel pending appointment
def cancel_appoint(request):
    try:
        response = {}
        appoint = Appointment.objects.get(id=request.GET['pk'])
        appoint.delete()
        response['status'] = 'success'
    except Exception:
        response['status'] = 'error'
    return HttpResponse(json.dumps(response),content_type="application/json")

def history(request):
    return render(request,"main/patient/history_book.html")

#get all appointment for selected date
def appoint_history(request):
    now  = datetime.now()
    first_day = datetime(int(request.GET['year']),int(request.GET['month']),1,0,0,0)
    end_day = first_day+relativedelta(months=+1)
    end_day = end_day - timedelta(days=1)
    appoints = Appointment.objects.filter(limit_date__gte = first_day).filter(limit_date__lte = end_day)
    if len(appoints) > 0:
        serialized_queryset = serializers.serialize('json', appoints)
        return HttpResponse(json.dumps(serialized_queryset),content_type="application/json")
    return HttpResponse(json.dumps(""),content_type="application/json")
        
def problems(request):
    return render(request,"main/patient/problems.html")

#get problems for selected month
def search_problems(request):
    now  = datetime.now()
    first = datetime(int(request.GET['year']),int(request.GET['month']),1,0,0,0)
    end = first+relativedelta(months=+1)
    end = end - timedelta(days=1)

    problems = Problem.objects.filter(pub_date__gte = first).filter(pub_date__lte = end)
    print(problems)
    if len(problems) > 0:
        serialized_queryset = serializers.serialize('json', problems)
        return HttpResponse(json.dumps(serialized_queryset),content_type="application/json")
    return HttpResponse(json.dumps(""),content_type="application/json")

#get details for selected problem        
def problems_detail(request):
    response = {}
    try:
        pk = request.GET['pk']
        problem = Problem.objects.get(id=pk)
        doctor_id = problem.doctor_id
        doctor = User.objects.get(id=doctor_id)
        response['doctor'] = doctor.first_name + " " + doctor.last_name
        response['pub_date'] = problem.pub_date.strftime('%Y-%m-%d')
        response['description'] = problem.description
    except Exception:
        response['doctor'] = 'error'
    return HttpResponse(json.dumps(response),content_type="application/json")


def medications(request):
    return render(request,"main/patient/medications.html")

#get medications for selected month
def search_medications(request):

    now  = datetime.now()
    first = datetime(int(request.GET['year']),int(request.GET['month']),1,0,0,0)
    end = first+relativedelta(months=+1)
    end = end - timedelta(days=1)

    medications = Medication.objects.filter(pub_date__gte = first).filter(pub_date__lte = end)
    if len(medications) > 0:
        serialized_queryset = serializers.serialize('json', medications)
        return HttpResponse(json.dumps(serialized_queryset),content_type="application/json")
    return HttpResponse(json.dumps(""),content_type="application/json")

#get details for selected medication
def medications_detail(request):
    response = {}
    try:
        pk = request.GET['pk']
        medication = Medication.objects.get(id=pk)
        doctor_id = medication.doctor_id
        doctor = User.objects.get(id=doctor_id)
        response['doctor'] = doctor.first_name + " " + doctor.last_name
        response['pub_date'] = medication.pub_date.strftime('%Y-%m-%d')
        response['description'] = medication.description    
        response['status'] = medication.status
    except Exception:
        response['doctor'] = 'error'
    return HttpResponse(json.dumps(response),content_type="application/json")

def tests(request):
    return render(request,"main/patient/tests.html")

# get test results for selected month
def search_tests(request):

    now  = datetime.now()
    first = datetime(int(request.GET['year']),int(request.GET['month']),1,0,0,0)
    end = first+relativedelta(months=+1)
    end = end - timedelta(days=1)

    tests = Test.objects.filter(pub_date__gte = first).filter(pub_date__lte = end)
    if len(tests) > 0:
        serialized_queryset = serializers.serialize('json', tests)
        return HttpResponse(json.dumps(serialized_queryset),content_type="application/json")
    return HttpResponse(json.dumps(""),content_type="application/json")

#get details for selected test
def tests_detail(request):
    response = {}
    try:
        pk = request.GET['pk']
        test = Test.objects.get(id=pk)
        doctor_id = test.doctor_id
        doctor = User.objects.get(id=doctor_id)
        response['doctor'] = doctor.first_name + " " + doctor.last_name
        response['pub_date'] = test.pub_date.strftime('%Y-%m-%d')
        response['description'] = test.description    
        response['name'] = test.name
        response['result'] = test.result
    except Exception:
        response['doctor'] = 'error'
    return HttpResponse(json.dumps(response),content_type="application/json")

############################################################################ medical site ###################################
#get incoming requested appointment
def incoming_requested(request):
    time_threshold = datetime.now()+timedelta(days=6)
    useremail = request.session['useremail']
    user = User.objects.get(useremail = useremail)
    accept_appoints = Appointment.objects.filter(doctor_id = user.id).filter(status='A').filter(limit_date__gt = datetime.now()).filter(limit_date__lt=time_threshold)
    if len(accept_appoints) > 0:
        serialized_queryset = serializers.serialize('json', accept_appoints)
        return HttpResponse(json.dumps(serialized_queryset),content_type="application/json")
    return HttpResponse(json.dumps(""),content_type="application/json")

#get all requested appointments
def requested_appoint(request):
    try:
        useremail = request.session['useremail']
        user = User.objects.get(useremail = useremail)
        userid = user.id
        appointments = Appointment.objects.filter(doctor_id = userid)
        if(len(appointments) > 0):
            return render(request,"main/medical/appointment.html",{"appointments":appointments})
    except Exception:
        pass
    return render(request,"main/medical/appointment.html")

#get appointment details for doctors        
def appoint_detailform(request):
    response = {}
    try:
        appoint = Appointment.objects.get(id=request.GET['pk'])
        user_id = appoint.user_id
        patient = User.objects.get(id = user_id)
        response['patient'] = patient.first_name + " " + patient.last_name
        response['pub_date'] = appoint.pub_date.strftime('%Y-%m-%d %H:%M')
        response['text'] = appoint.book_text
    except Exception:
        response['patient'] = 'error'
    return HttpResponse(json.dumps(response),content_type="application/json")

#accpet or reject appointment
def appoint_action(request):
    response = {}
    try:
        appoint = Appointment.objects.get(id=request.GET['pk'])
        if request.GET['method'] == 'A':
            appoint.status = 'A'
        else:
            appoint.status = 'R'
        appoint.save()
        response['status'] = 'success'
    except Exception:
        response['status'] = 'error'
    return HttpResponse(json.dumps(response),content_type="application/json")

#get patient information
def patient_info(request):
    try:
        pk = request.GET['pk']
        appoint = Appointment.objects.get(id=pk)
        user_id = appoint.user_id
        patient_data = User.objects.get(id=user_id)
        tests = Test.objects.filter(user_id = user_id)
        medications = Medication.objects.filter(user_id = user_id)
        problems = Problem.objects.filter(user_id = user_id)

        return render(request,"main/medical/patient_info.html",{"patient_data":patient_data,"tests":tests,"medications":medications,"problems":problems})
    except Exception:
        pass    
    return redirect("main:dashboard")

#save problem
def save_problem(request):
    response = {}
    try:
        pk = request.GET['pk']
        text = request.GET['text']
        problem = Problem.objects.get(id = pk)
        problem.description = text
        problem.save()
        response['status'] = 'success'
    except Exception:
        response['status'] = 'error'
    return HttpResponse(json.dumps(response),content_type="application/json") 

#add new problem for patient
def create_problem(request):
    response = {}
    try:
        useremail = request.session['useremail']
        mode = request.GET['mode']
        doctor = User.objects.get(useremail = useremail)
        text = request.GET['text']
        if int(mode) == 0:
            appoint_id = request.GET['pk']
            appoint = Appointment.objects.get(id = appoint_id)
            problem = Problem(user_id=appoint.user_id,doctor_id=doctor.id,description=text)
            problem.save()
        else:
            problem = Problem(user_id=request.GET['pk'],doctor_id=doctor.id,description=text)
            problem.save()

        response['status'] = 'success'
    except Exception:
        response['status'] = 'error'
    return HttpResponse(json.dumps(response),content_type="application/json") 

#save medication 
def save_medication(request):
    response = {}
    try:
        pk = request.GET['pk']
        text = request.GET['text']
        status = request.GET['status']
        medication = Medication.objects.get(id = pk)
        medication.description = text
        medication.status = status
        medication.save()
        response['status'] = 'success'
    except Exception:
        response['status'] = 'error'
    return HttpResponse(json.dumps(response),content_type="application/json") 

#add new medication for patient
def create_medication(request):
    response = {}
    try:
        useremail = request.session['useremail']
        doctor = User.objects.get(useremail = useremail)
        text = request.GET['text']
        status = request.GET['status']
        mode = request.GET['mode']
        if int(mode) == 0:
            appoint_id = request.GET['pk']
            appoint = Appointment.objects.get(id = appoint_id)
            medication = Medication(user_id=appoint.user_id,doctor_id=doctor.id,description=text,status = status)
            medication.save()
        else:
            medication = Medication(user_id=request.GET['pk'],doctor_id=doctor.id,description=text,status = status)
            medication.save()

        response['status'] = 'success'
    except Exception:
        response['status'] = 'error'
    return HttpResponse(json.dumps(response),content_type="application/json") 

#save test
def save_test(request):
    response = {}
    try:
        pk = request.GET['pk']
        text = request.GET['text']
        name = request.GET['name']
        result = request.GET['result']
        test = Test.objects.get(id = pk)
        test.description = text
        test.name = name
        test.result = result
        test.save()
        response['status'] = 'success'
    except Exception:
        response['status'] = 'error'
    return HttpResponse(json.dumps(response),content_type="application/json") 

#add new test for patient
def create_test(request):
    response = {}
    try:
        useremail = request.session['useremail']
        doctor = User.objects.get(useremail = useremail)
        text = request.GET['text']
        result = request.GET['result']
        name = request.GET['name']
        mode = request.GET['mode']
        if int(mode) == 0:
            appoint_id = request.GET['pk']
            appoint = Appointment.objects.get(id = appoint_id)
            test = Test(user_id=appoint.user_id,doctor_id=doctor.id,name=name,description=text,result = result)
            test.save()
        else:
            test = Test(user_id=request.GET['pk'],doctor_id=doctor.id,name=name,description=text,result = result)
            test.save()

        response['status'] = 'success'
    except Exception:
        response['status'] = 'error'
    return HttpResponse(json.dumps(response),content_type="application/json") 

#get all patients
def user_info(request):
    users = User.objects.filter(user_type='PA')
    return render(request,"main/medical/health_info.html",{"users":users})

#search patients by name or birthday
def search_patients(request):
    year =""
    month = ""
    day = ""
    try:
        year = request.GET['year']
    except Exception:
        pass
    try:
        month = request.GET['month']
    except Exception:
        pass
    try:
        day = request.GET['day']
    except Exception:
        pass

    # search by only year
    if month == "":
        start = datetime(int(year),1,1,0,0,0)
        end = datetime(int(year),12,31,0,0,0)
        users = User.objects.filter(user_type = 'PA').filter(birthday__gte = start).filter(birthday__lte = end).order_by('-birthday')
        if len(users) > 0:
            serialized_queryset = serializers.serialize('json', users)
            return HttpResponse(json.dumps(serialized_queryset),content_type="application/json")
    elif month != "" and day == "":
        pattern = str(year) + "-" +str(month).zfill(2)
        users = User.objects.filter(user_type = 'PA').filter(birthday__contains=pattern).order_by('-birthday')
        if len(users) > 0:
            serialized_queryset = serializers.serialize('json', users)
            return HttpResponse(json.dumps(serialized_queryset),content_type="application/json")
    elif month != "" and day != "":
        date_filter = datetime(int(year),int(month),int(day),0,0,0)
        users = User.objects.filter(user_type = 'PA').filter(birthday = date_filter).order_by('-birthday')
        if len(users) > 0:
            serialized_queryset = serializers.serialize('json', users)
            return HttpResponse(json.dumps(serialized_queryset),content_type="application/json")
    return HttpResponse(json.dumps(""),content_type="application/json")
    
#search patient by name
def search_patients_name(request):
    first = ""
    last = ""
    try:
        first = request.GET['first_name']
        first = first.strip()
    except Exception:
        pass
    try:
        last = request.GET['last_name']
        last = last.strip()
    except Exception:
        pass
    if first == "" and last == "":
        users = User.objects.filter(user_type='PA')
        if len(users) > 0:
            serialized_queryset = serializers.serialize('json', users)
            return HttpResponse(json.dumps(serialized_queryset),content_type="application/json")
    elif first != "" and last == "":
        users = User.objects.filter(user_type='PA').filter(first_name__contains=first)
        if len(users) > 0:
            serialized_queryset = serializers.serialize('json', users)
            return HttpResponse(json.dumps(serialized_queryset),content_type="application/json")
    elif first == "" and last != "":
        users = User.objects.filter(user_type='PA').filter(last_name__contains=last)
        if len(users) > 0:
            serialized_queryset = serializers.serialize('json', users)
            return HttpResponse(json.dumps(serialized_queryset),content_type="application/json")
    elif first != "" and last != "":
        users = User.objects.filter(user_type='PA').filter(first_name__contains=first).filter(last_name__contains=last)
        if len(users) > 0:
            serialized_queryset = serializers.serialize('json', users)
            return HttpResponse(json.dumps(serialized_queryset),content_type="application/json")
    return HttpResponse(json.dumps(""),content_type="application/json")

#go to patient information page
def patient_info_user(request):
    try:
        user_id = request.GET['pk']
        patient_data = User.objects.get(id=user_id)
        tests = Test.objects.filter(user_id = user_id)
        medications = Medication.objects.filter(user_id = user_id)
        problems = Problem.objects.filter(user_id = user_id)

        return render(request,"main/medical/patient_info.html",{"patient_data":patient_data,"tests":tests,"medications":medications,"problems":problems})
    except Exception:
        pass    
    return redirect("main:dashboard")


#########################################################################################################################

# go to doctor management page
def doctor(request):
    try:
        users = User.objects.filter(user_type='MD')
        return render(request,"main/admin/doctor.html",{"users":users})
    except Exception:
        pass
    return redirect("main:dashboard")

#search doctors by name or birthday
def search_doctors_birth(request):
    year =""
    month = ""
    day = ""
    try:
        year = request.GET['year']
    except Exception:
        pass
    try:
        month = request.GET['month']
    except Exception:
        pass
    try:
        day = request.GET['day']
    except Exception:
        pass

    # search by only year
    if month == "":
        start = datetime(int(year),1,1,0,0,0)
        end = datetime(int(year),12,31,0,0,0)
        users = User.objects.filter(user_type = 'MD').filter(birthday__gte = start).filter(birthday__lte = end).order_by('-birthday')
        if len(users) > 0:
            serialized_queryset = serializers.serialize('json', users)
            return HttpResponse(json.dumps(serialized_queryset),content_type="application/json")
    elif month != "" and day == "":
        pattern = str(year) + "-" +str(month).zfill(2)
        users = User.objects.filter(user_type = 'MD').filter(birthday__contains=pattern).order_by('-birthday')
        if len(users) > 0:
            serialized_queryset = serializers.serialize('json', users)
            return HttpResponse(json.dumps(serialized_queryset),content_type="application/json")
    elif month != "" and day != "":
        date_filter = datetime(int(year),int(month),int(day),0,0,0)
        users = User.objects.filter(user_type = 'MD').filter(birthday = date_filter).order_by('-birthday')
        if len(users) > 0:
            serialized_queryset = serializers.serialize('json', users)
            return HttpResponse(json.dumps(serialized_queryset),content_type="application/json")
    return HttpResponse(json.dumps(""),content_type="application/json")
    
#search doctor by name
def search_doctors_name(request):
    first = ""
    last = ""
    try:
        first = request.GET['first_name']
        first = first.strip()
    except Exception:
        pass
    try:
        last = request.GET['last_name']
        last = last.strip()
    except Exception:
        pass
    if first == "" and last == "":
        users = User.objects.filter(user_type='MD')
        if len(users) > 0:
            serialized_queryset = serializers.serialize('json', users)
            return HttpResponse(json.dumps(serialized_queryset),content_type="application/json")
    elif first != "" and last == "":
        users = User.objects.filter(user_type='MD').filter(first_name__contains=first)
        if len(users) > 0:
            serialized_queryset = serializers.serialize('json', users)
            return HttpResponse(json.dumps(serialized_queryset),content_type="application/json")
    elif first == "" and last != "":
        users = User.objects.filter(user_type='MD').filter(last_name__contains=last)
        if len(users) > 0:
            serialized_queryset = serializers.serialize('json', users)
            return HttpResponse(json.dumps(serialized_queryset),content_type="application/json")
    elif first != "" and last != "":
        users = User.objects.filter(user_type='MD').filter(first_name__contains=first).filter(last_name__contains=last)
        if len(users) > 0:
            serialized_queryset = serializers.serialize('json', users)
            return HttpResponse(json.dumps(serialized_queryset),content_type="application/json")
    return HttpResponse(json.dumps(""),content_type="application/json")

def get_userinfo(request):
    try:
        pk = request.GET['pk']
        user = User.objects.filter(id = pk)
        if len(user) > 0:
            serialized_queryset = serializers.serialize('json', user)
            return HttpResponse(json.dumps(serialized_queryset),content_type="application/json")
    except Exception:
        pass
    return HttpResponse(json.dumps(""),content_type="application/json")

def save_userinfo(request):
    response = {}
    try:
        pk = request.GET['pk']
        first_name = request.GET['first_name']
        last_name = request.GET['last_name']
        birthday = request.GET['birthday']
        gender = request.GET['gender']
        email = request.GET['email']
        phone = request.GET['phone']
        postcode = request.GET['postcode']
        address = request.GET['address']
        practice = request.GET['practice']
        profession = ""
        try:
            profession = request.GET['profession']
        except Exception:
            pass


        user = User.objects.get(id=pk)
        user.first_name = first_name
        user.last_name = last_name
        user.birthday = birthday
        user.gender = gender
        user.useremail = email
        user.phone_number = phone
        user.postcode = postcode
        user.address = address
        user.practice = practice
        user.profession = profession

        user.save()
        response['status'] = 'success'
    except Exception:
        response['status'] = 'error'
    return HttpResponse(json.dumps(response),content_type="application/json")
    
def block_user(request):
    response = {}
    try:
        pk = request.GET['pk']
        user = User.objects.get(id=pk)
        user.delete()
        response['status'] = 'success'
    except Exception:
        response['status'] = 'error'
    return HttpResponse(json.dumps(response),content_type="application/json")

def add_doctor(request):
    response = {}
    try:
        first_name = request.GET['first_name']
        last_name = request.GET['last_name']
        password = request.GET['password']
        birthday = request.GET['birthday']
        gender = request.GET['gender']
        email = request.GET['email']
        phone = request.GET['phone']
        postcode = request.GET['postcode']
        address = request.GET['address']
        practice = request.GET['practice']
        profession = request.GET['profession']

        user = User(first_name=first_name,last_name = last_name,password = make_password(password), birthday = birthday,gender = gender,useremail=email,phone_number = phone, postcode = postcode,address = address,practice=practice,profession=profession,is_active = 0,user_type='MD')
        user.save()
        response['status'] = 'success'
    except Exception:
        response['status'] = 'error'
    return HttpResponse(json.dumps(response),content_type="application/json")
    
def patient(request):
    users = User.objects.filter(user_type='PA')
    return render(request,"main/admin/patient.html",{"users":users})
    
def add_patient(request):
    response = {}
    try:
        first_name = request.GET['first_name']
        last_name = request.GET['last_name']
        password = request.GET['password']
        birthday = request.GET['birthday']
        gender = request.GET['gender']
        email = request.GET['email']
        phone = request.GET['phone']
        postcode = request.GET['postcode']
        address = request.GET['address']
        practice = request.GET['practice']

        user = User(first_name=first_name,last_name = last_name,password = make_password(password), birthday = birthday,gender = gender,useremail=email,phone_number = phone, postcode = postcode,address = address,practice=practice,is_active = 0,user_type='PA')
        user.save()
        response['status'] = 'success'
    except Exception:
        response['status'] = 'error'
    return HttpResponse(json.dumps(response),content_type="application/json")

def patient_info_user_admin(request):
    try:
        user_id = request.GET['pk']
        patient_data = User.objects.get(id=user_id)
        tests = Test.objects.filter(user_id = user_id)
        medications = Medication.objects.filter(user_id = user_id)
        problems = Problem.objects.filter(user_id = user_id)

        return render(request,"main/admin/patient_info.html",{"patient_data":patient_data,"tests":tests,"medications":medications,"problems":problems})
    except Exception:
        pass    
    return redirect("main:dashboard")

#reset user password
def change_password(request):
    response = {}
    try:
        pk = request.GET['pk']
        password = request.GET['password']

        user = User.objects.get(pk=pk)
        user.password = make_password(password)
        user.save()
        response['status'] = 'success'
    except Exception:
        response['status'] = 'error'
    return HttpResponse(json.dumps(response),content_type="application/json")
    




