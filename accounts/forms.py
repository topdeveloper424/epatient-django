from django import forms
from django.forms import ModelForm
from .models import User

class SingupForm(ModelForm):
    class Meta:
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

        model = User
        fields = ['first_name','last_name','birthday','gender','postcode','address','practice','useremail','password','phone_number','user_type']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control','placeholder':'Please type your given name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control','placeholder':'Please type family name'}),
            'birthday': forms.DateInput(attrs={'class': 'form-control','type':'date','placeholder':'Please type family name'}),
            'gender': forms.Select(attrs={'class': 'form-control select2-single'},choices=GENDER),
            'postcode': forms.TextInput(attrs={'class': 'form-control','placeholder':'Please type post code'}),
            'address': forms.TextInput(attrs={'class': 'form-control','placeholder':'Please type address'}),
            'practice': forms.Textarea(attrs={'class': 'form-control','placeholder':'Please type your practice'}),

            'useremail': forms.TextInput(attrs={'class': 'form-control','type':'email','placeholder':'Please type your email'}),
            'password': forms.TextInput(attrs={'class': 'form-control','type':'password','placeholder':'Please type your password'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control','placeholder':'Please type your phone number'}),
            'user_type':forms.TextInput(attrs={'type':'hidden','value':PATIENT})
        }
    def save(self, commit=True):
        user  = super(ModelForm, self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.useremail = self.cleaned_data['useremail']

        if commit:
            user.save()
        return user

