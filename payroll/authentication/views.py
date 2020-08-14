from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth import authenticate, login, logout

from employee_management.models import *

from .auth_backend import AuthBackend
from .models import *
from .forms import *


def loginto(request, invalid="False"):
    is_valid = None

    if request.method == 'POST':
        form = login_form(request.POST)

        if form.is_valid():
            cd = form.cleaned_data
            user_auth = authenticate(name=cd['name'],
                                     password=cd['password'],
                                     institution_name=cd['company_name'])

            if user_auth is not None:
                if user_auth.is_active:
                    login(request, user_auth)
                    if isinstance(user_auth, (Users,)):
                        return redirect('dashboard_payroll')
                    else:
                        redirect('check_in_employee',
                                 employee_name=user_auth.name)
            else:
                return redirect('login', invalid="True")
    else:
        if invalid == "True":
            is_valid = "True"

        form = login_form()
    return render(request, 'login.html', {'form': form, 'is_valid': is_valid})


def signup(request):

    if request.method == "POST":

        form = signup_form(request.POST)

        if form.is_valid():
            cd = form.cleaned_data
            Users.objects.create_user(cd["user_name"],
                                      cd["email"],
                                      cd["company_name"],
                                      cd["password"])

            return redirect("dashboard_payroll")
    else:
        form = signup_form()

    return render(request,"signup.html",{"form":form})


def create_firm(request):

    if request.method == "POST":

        form = firm_form(request.POST)

        if form.is_valid():
            form.save()
            return redirect("/authentication/login")
        else:
            return HttpResponse(form.errors)
    else:
        form = firm_form()

    return render(request, "institution.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect('login')


def employee_login(request, invalid=False):
    is_valid = None

    if request.method == 'POST':
        form = login_form(request.POST)

        if form.is_valid():
            cd = form.cleaned_data
            user_auth = authenticate(name=cd['name'],
                                     password=cd['password'],
                                     institution_name=cd['company_name'])

            if user_auth is not None:
                if user_auth.is_active:
                    login(request, user_auth)
                    return redirect('employee_checkin',
                                    employee_name=user_auth.full_name)
                return redirect('login', invalid="True")
    else:
        if invalid == "True":
            is_valid = "True"

        form = login_form()
    return render(request, 'login.html', {'form': form, 'is_valid': is_valid})


def get_logged_in_user(request):
    return request.user.firm_name
