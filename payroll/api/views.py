import calendar
from rest_framework import generics

from django.shortcuts import render

from employee_management.models import *
from employee_management.builder import EmployeeBuilder
from payroll_management.models import *

from .serializers import *


class EmployeeListView(generics.ListAPIView):
    serializer_class = EmployeeSerializer

    def get_queryset(self):
        if self.kwargs.get("employee_name")!=None:
            return Employee.objects.filter(full_name=self.kwargs["employee_name"])
        return Employee.objects.all()


class PaySlipListView(generics.ListAPIView):

    queryset = PaySlip.objects.all()
    serializer_class = PaySlipSerializer


class PaySlipListByNameView(generics.ListAPIView):

    serializer_class = PaySlipSerializer

    def get_queryset(self):
        employee = EmployeeBuilder.get_employee_static(self.kwargs["employee_name"])
        return PaySlip.objects.filter(employee=employee)

def get_month_number(month):
    abbr_to_num = {name: num for num, name in enumerate(calendar.month_abbr) if num}
    month_number = abbr_to_num[month.capitalize()[:3]]
    return month_number

class PaySlipListByMonthView(generics.ListAPIView):

    serializer_class = PaySlipSerializer

    def get_queryset(self):
        month_number = get_month_number(self.kwargs["month_name"])
        
        return PaySlip.objects.filter(date_created__month=month_number)
