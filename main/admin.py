from django.contrib import admin
from main.models import Appointment,Test,Problem,Medication
# Register your models here.

admin.site.register(Appointment)
admin.site.register(Test)
admin.site.register(Problem)
admin.site.register(Medication)
