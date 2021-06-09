from django import forms
from django.shortcuts import redirect, render
from .forms import UserRegisterForm
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.

def register(request):
    if request.method=='POST':
        form=UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username=form.cleaned_data.get('username')
            messages.success(request,f'Your account has been created successfully! You are now able to Login ')
            return redirect('user-login')
    else:
        form=UserRegisterForm()
    return render(request,'users/register.html',{'form':form})


