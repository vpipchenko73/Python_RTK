from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.validators import EmailValidator
from main.models import Account
#from bootstrap_datepicker_plus import DatePickerInput


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(label='Email', validators=[EmailValidator()])

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']




class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['nickname', 'birthdate', 'gender', 'account_image']
        widgets = {
                   'nickname': forms.TextInput({'class': 'textinput form-control', 'placeholder': 'Введите свой ник'}),
                   #'birthdate': forms.DateField( ),
                   'birthdate': forms.DateInput(format='%d/%m/%Y', attrs={"type": "date"}),
                   'gender': forms.Select( ),
                   'account_image': forms.FileInput({'class': 'form-control', 'placeholder': 'image'})
                   }


