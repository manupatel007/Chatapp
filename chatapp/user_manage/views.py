from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.urls import reverse
from user_manage.forms import CustomUserCreationForm
from django.http import HttpResponse


# Create your views here.
def dashboard(request):
    return render(request,"users/dashboard.html",{})

def registration(request):
    if request.method=='GET':
        return render(
            request, "users/register.html",
            {'form':CustomUserCreationForm}
            )
    elif request.method=='POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request,user)
            return redirect(reverse('chat_home'))
        else:
            return HttpResponse("Username is already taken")