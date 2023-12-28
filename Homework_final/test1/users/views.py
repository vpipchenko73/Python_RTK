from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.models import Group
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import UserRegistrationForm, AccountForm
from main.models import Account
from django.contrib.auth.decorators import login_required


#from .models import BaseRegisterForm
# Create your views here.

def registration(request):
    if request.method=='POST':
        #form = UserCreationForm(request.POST)
        form = UserRegistrationForm(request.POST)

        if form.is_valid():
            user = form.save() #появляется новый пользователь
            category = request.POST['account_type']
            if category == 'author':
                group = Group.objects.get(name='Actions Required')
                user.groups.add(group)
            else:
                group = Group.objects.get(name='Reader')
                user.groups.add(group)
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            account = Account.objects.create(user=user, nickname=user.username)
            email = form.cleaned_data.get('email')

            #!!!не аутентифицируется - нужно доделать
            authenticate(username=username,password=password)
            login(request, user)
            messages.success(request,f'{username} был зарегистрирован!')
            return redirect('index')
    else:
        form = UserRegistrationForm()
    context = {'form':form}
    return render(request,'users/registration.html',context)

@login_required(login_url='index')
def profile_update(request):
    user = request.user
    print (user)
    account = Account.objects.get(user=user)
    print(account)
    if request.method == "POST":
        #user_form = AccountForm(request.POST, instance=user)
        #account_form = AccountUpdateForm(request.POST, request.FILES, instance=account)
        account_form = AccountForm(request.POST, request.FILES, instance=account)
        #account_form = AccountForm(request.POST)
        if account_form.is_valid():
            account_form.save()
            messages.success(request,"Профиль успешно обновлен")
            print(request.POST)

            return redirect('account')
        else:
            print (' (((')
    else:
        context = {'account_form':AccountForm(instance=account), 'account': account}
    return render(request,'users/account.html',context)


class AccountUpdateView(UpdateView):
    model = Account
    fields = ['nickname', 'birthdate', 'gender', 'account_image']
    context_object_name ='account'
    template_name = 'users/account.html'

