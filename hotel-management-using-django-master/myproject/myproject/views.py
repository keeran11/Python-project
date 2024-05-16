from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
# from django.urls import reverse
from django.views.generic import TemplateView


def userlogin(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return redirect('myapp:main_backend_page')
            else:
                return HttpResponse("Account not create")
        else:
            print("Someone tried to login and falied!")
            print("They used username: {} and password: {}".format(username, password))
            return HttpResponse("Invalid login details given")
    else:
        return render(request, 'Backend/login.html', {})





