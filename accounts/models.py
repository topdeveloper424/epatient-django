from django.db import models

from datetime import date

# Create your models here.
class User(models.Model):
    ADMIN = 'AD'
    MEDICAL = 'MD'
    PATIENT = 'PA'
    USER_IN_HOSPITAL_CHOICES = (
        (ADMIN, 'Administrator'),
        (MEDICAL,'medical'),
        (PATIENT,'patient'),
    )
    GENDER = (
        ('M', 'male'),
        ('F','female'),
    )

    first_name = models.CharField(max_length=200, null = False, default='')
    last_name = models.CharField(max_length=200, null = False, default='')
    birthday = models.DateField(null=False,default=date.today)
    gender = models.CharField(max_length = 2, choices = GENDER, default = 'M')
    postcode = models.CharField(max_length = 100,null=False,default='')
    address = models.CharField(max_length=254, null = False, default='')
    practice = models.CharField(max_length=254, null = True, default='')
    profession = models.CharField(max_length=254, null = True, default='')
 
    useremail = models.EmailField(blank=False, unique=True, default='')
    password = models.CharField(max_length=200, null = False, default='')
    user_type = models.CharField(max_length = 2, choices = USER_IN_HOSPITAL_CHOICES, default = PATIENT)
    phone_number = models.CharField(max_length = 200 ,null=False,unique=True, default = '')
    verify_code = models.CharField(max_length = 10, null = True)
    verify_time = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=False)

