from django.db import models

# Create your models here.
from datetime import date


class Appointment(models.Model):            #appointment model
    PENDING = 'P'
    ACCEPTED = 'A'
    REJECTED = 'R'
    STATUS_CHOICES = (
        (PENDING, 'pending'),
        (ACCEPTED,'accepted'),
        (REJECTED,'rejected'),
    )

    user_id = models.IntegerField()
    doctor_id = models.IntegerField()
    book_date = models.DateField()
    from_time = models.TimeField()
    to_time=models.TimeField()
    limit_date = models.DateTimeField(null=True,blank=True)
    book_text = models.TextField()
    status = models.CharField(max_length = 2, choices = STATUS_CHOICES, default = PENDING)
    pub_date = models.DateTimeField(auto_now_add=True)

class Problem(models.Model):                #Problem model
    user_id = models.IntegerField()
    doctor_id = models.IntegerField()
    description = models.TextField()
    pub_date = models.DateField(auto_now_add=True)

class Medication(models.Model):             #Medication model
    ACUTE = 'A'
    REPEAT = 'R'
    STATUS_CHOICES = (
        (ACUTE, 'acute'),
        (REPEAT,'repeat'),
    )


    user_id = models.IntegerField()
    doctor_id = models.IntegerField()
    description = models.TextField()
    status = models.CharField(max_length = 2, choices = STATUS_CHOICES, default = ACUTE)
    pub_date=models.DateField(auto_now_add=True)

class Test(models.Model):                   #Test model
    user_id = models.IntegerField()
    doctor_id = models.IntegerField()
    name = models.CharField(max_length = 50)
    description = models.TextField()
    result = models.CharField(max_length = 200)
    pub_date=models.DateField(auto_now_add=True)
    

    
    



