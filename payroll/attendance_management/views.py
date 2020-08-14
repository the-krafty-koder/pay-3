import requests
import socket
import os
import datetime

from django.views.generic import (ListView,
                                  DetailView)
from django.shortcuts import (render,
                              redirect,
                              HttpResponse,
                              get_object_or_404)
from django.utils import timezone
from django.views import View
from django.core.paginator import Paginator

from functools import wraps
from ipware import get_client_ip

from employee_management.forms import SearchForm
from api.views import get_month_number

from .manager import (AttendanceManager,
                      AttendanceBuilder)
from .models import DailyAttendance
from .locator import *


def validate_ip(address):
    try:
        socket.inet_aton(address)
        return True
    except socket.error:
        return False


def create_daily_attendance(request):
    is_absent = list(DailyAttendance.objects.filter(date_created=timezone.localdate()))==[]

    if is_absent:
        daily_attendance = DailyAttendance.objects.create()
        attendance_manager = AttendanceManager(daily_attendance)

    return redirect('attendance_list')


def list_attendance(request, date=None):
    daily_attendance = AttendanceBuilder.get_attendance()

    if date:
        daily_attendance = DailyAttendance.objects.filter(date_created=date)

    return render(request,"list_attendance.html", {"daily_attendance":daily_attendance})


def attendance_dashboard(request):
    is_absent = list(DailyAttendance.objects.filter(date_created=timezone.localdate()))==[]

    if is_absent is False:
        return redirect('attendance_list')

    return render(request, "initial.html")


def find_employee_ip(func):
    """if longitude:
        return HttpResponse(longitude,latitude)
    ip = None
    client_ip, is_routable = get_client_ip(request)
    if client_ip is None:
        # Unable to get the client's IP address'
        return HttpResponse("Ip address not found!")
    else:
        # We got the client's IP address
        if is_routable:  # The client's IP address is publicly
        routable on the Internet
            client_ip = ip
        #else:
            # The client's IP address is private
            #return HttpResponse("Ip address is private!")"""

    @wraps(func)
    def wrapper(request, *args, **kwargs):
        employee_name = kwargs.get("employee_name")

        # ip = requests.get('https://checkip.amazonaws.com'). text.strip()
        # remove on production!!
        coordinates = (GetLocationDetails().get_geoposition())

        if check_if_in_radius((1.391259, 36.940388), coordinates):
            f = func(request, employee_name)
            return f
        return HttpResponse("Accept First")

    return wrapper


@find_employee_ip
def employee_check_in(request, employee_name):

    manager = AttendanceManager(AttendanceBuilder.get_attendance())
    check_in = manager.check_attendance_object(employee_name)

    return render(request, "employee_check_in.html",{"check_in":check_in,"employee_name":employee_name})


def employee_checkin_toggle(request,employee_name):

    manager = AttendanceManager(AttendanceBuilder.get_attendance())
    manager.toggle_attendance_object(employee_name)

    return redirect('check_in_employee', employee_name=employee_name)


def validate(request, employee_name):
    return render(request, "trial.html")


def check_in_declined(request):
    return HttpResponse("You have to accept ")


class DailyAttendanceListview(View):
    form_class = SearchForm
    context_object_name = "attendance_records"
    template_name = "list_records.html"

    def get(self, request, *args, **kwargs):
        form, date = self.form_class(), kwargs.get("date")
        records = DailyAttendance.objects.filter()

        paginator = Paginator(records, 8)
        page_number = request.GET.get('page')
        records = paginator.get_page(page_number)

        if date is not None:
            date = date.split("-")
            date_created = datetime.datetime(int(date[2]), int(date[1]), int(date[0]))
            records = DailyAttendance.objects.filter(date_created=date_created)

        return render(request, self.template_name, {"form":form,"attendance_records":records})

    def post(self,request,*args,**kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data["search_text"].split(" ")
            date = f"{cd[0]}-{get_month_number(cd[1])}-{cd[2]}"
            return redirect('attendance_records', date=date)


class DailyAttendanceDetailView(DetailView):
    context_object_name = "attendance_record"

    def get_queryset(self):
        return get_object_or_404(DailyAttendance, id=self.kwargs['id'])
