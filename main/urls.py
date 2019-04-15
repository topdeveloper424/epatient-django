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

app_name = 'main'

urlpatterns = [
    path('', views.index,name='index'),

    path('view-profile', views.view_profile,name='view_profile'),

    path('dashboard', views.dashboard,name='dashboard'),
############################################################ patient sites ################################
    path('incoming-appoint', views.incoming_appoint,name='incoming_appoint'),

    path('appointment/book', views.book,name='book'),
    path('search-doctors', views.searchDoctors,name='searchDoctors'),
    path('create-book', views.create_book,name='create_book'),

    path('appointment/view', views.view_book,name='view'),
    path('appoint-detail', views.appoint_detail,name='appoint_detail'),
    path('change-appoint', views.change_appoint,name='change_appoint'),
    path('cancel-appoint', views.cancel_appoint,name='cancel_appoint'),

    path('appointment/history', views.history,name='history'),
    path('appoint-history', views.appoint_history,name='appoint_history'),

    path('healthinfo/problems', views.problems,name='problems'),
    path('search-problems', views.search_problems,name='search_problems'),
    path('problems-detail', views.problems_detail,name='problems_detail'),

    path('healthinfo/medications', views.medications,name='medications'),
    path('search-medications', views.search_medications,name='search_medications'),
    path('medications-detail', views.medications_detail,name='medications_detail'),

    path('healthinfo/tests', views.tests,name='tests'),
    path('search-tests', views.search_tests,name='search_tests'),
    path('tests-detail', views.tests_detail,name='tests_detail'),

######################################################################################################
    path('incoming-requested', views.incoming_requested,name='incoming_requested'),
    path('appointment/requested-appoint', views.requested_appoint,name='requested_appoint'),
    path('appoint-detailform', views.appoint_detailform,name='appoint_detailform'),
    path('appoint-action', views.appoint_action,name='appoint_action'),

    path('patient-info', views.patient_info,name='patient_info'),

    path('save-problem', views.save_problem,name='save_problem'),
    path('create-problem', views.create_problem,name='create_problem'),

    path('save-medication', views.save_medication,name='save_medication'),
    path('create-medication', views.create_medication,name='create_medication'),

    path('save-test', views.save_test,name='save_test'),
    path('create-test', views.create_test,name='create_test'),

    path('healthinfo/users',views.user_info,name='user_info'),
    path('search-patients',views.search_patients,name='search_patients'),
    path('search-patients-name',views.search_patients_name,name='search_patients_name'),

    path('patient-info-user', views.patient_info_user,name='patient_info_user'),


###########################################################################################
    
    path('management/doctor', views.doctor,name='doctor'),
    path('management/patient', views.patient,name='patient'),
    path('search-doctors-birth',views.search_doctors_birth,name='search_doctors_birth'),
    path('search-doctors-name',views.search_doctors_name,name='search_doctors_name'),

    path('get-userinfo',views.get_userinfo,name='get_userinfo'),
    path('save-userinfo',views.save_userinfo,name='save_userinfo'),

    path('block-user',views.block_user,name='block_user'), # block user ajax
    path('add-doctor',views.add_doctor,name='add_doctor'), # add user ajax

    path('add-patient',views.add_patient,name='add_patient'), # add user ajax

    path('patient-info-user-admin', views.patient_info_user_admin,name='patient_info_user_admin'),
    path('change-password', views.change_password,name='change_password'),


]
