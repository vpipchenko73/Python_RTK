from django.forms import ModelForm, BooleanField, Form
from .models import Article, Image
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm, AuthenticationForm
from django.forms import TextInput, CharField, Textarea, CheckboxSelectMultiple, Select, SelectMultiple
from django import forms
from django.forms import inlineformset_factory
from django.core.validators import MinLengthValidator


# сщздаем модельную форму

class ArticleForm_Detail(ModelForm):
    # check_box=BooleanField(label='Подтвердите')
    # в класс мета заносим модель и нужные нам поля
    class Meta:
        model = Article
        fields = ['author', 'title', 'text', 'category']

class ArticleFormCreate(ModelForm):
    check_box=BooleanField(label='Подтвердите')
    # в класс мета заносим модель и нужные нам поля
    class Meta:
        model=Article
        fields=['author', 'title', 'anouncement','text', 'category', 'tags' ,'check_box'] # 'date',


# class UserAuthForm(AuthenticationForm):
#
#       class Meta:
#         model = User
#
#         fields = ['username', 'password']
#         widgets = {'username': TextInput({'class': 'textinput form-control','placeholder': 'username'}) }
#         #widget= {'username': TextInput( attrs={'autocomplete':'off',} )}

class UserAuthForm(forms.Form):
        #username = forms.CharField(label='Username',initial = 'First Name', max_length=50)
        username = forms.CharField(label='Username', max_length=50,
                                   widget=forms.TextInput(attrs={'style': 'background: #f2f2f2; border: 2px solid black' }))
        password = forms.CharField(label='Password', max_length=50,
                                   widget=forms.TextInput(attrs={'id': 'asdform', "type": "password"}))




class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result



ImagesFormSet = inlineformset_factory(Article, Image, fields=("image",),extra=1,max_num=4,
                                      widgets={"image_field": MultipleFileField()})

class ArticleForm(ModelForm):
    image_field = MultipleFileField(label='Выберете иллюстрации к новости')

    class Meta:
        model = Article
        fields = ['title','anouncement','text','category','tags']
        widgets = {
            'title': Textarea(attrs={'cols': 80, 'rows': 1, 'style': 'background: #f2f2f2; border: 2px solid black'}),
            'anouncement': Textarea(attrs={'cols':80,'rows':1, 'style': 'background: #f2f2f2; border: 2px solid black' }),
            'text': Textarea(attrs={'rows': 5, 'style': 'background: #f2f2f2; border: 2px solid black' }),
            'category': Select(attrs={'style': 'background: #f2f2f2; border: 2px solid black'}),
            #'tags': CheckboxSelectMultiple(),
            'tags': SelectMultiple(attrs={'style': 'background: #f2f2f2; border: 2px solid black' }),
            'author': Select(attrs={'style': 'background: #f2f2f2; border: 2px solid black' })
        }