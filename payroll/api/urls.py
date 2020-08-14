
from django.urls import path
from .views import (
    EmployeeListView,
    PaySlipListView,
    PaySlipListByNameView,
    PaySlipListByMonthView
)

urlpatterns = [
    path('employees/', EmployeeListView.as_view(), name="employee_list_api"),

    path('employees/<str:employee_name>', EmployeeListView.as_view(),
         name="employee_list_api"),

    path('payroll/payslips', PaySlipListView.as_view(),
         name="payslip_list_api"),

    path('payroll/payslips/employee/<str:employee_name>',
         PaySlipListByNameView.as_view(), name="payslip_list_by_name"),

    path('payroll/payslips/month/<str:month_name>',
         PaySlipListByMonthView.as_view(), name="payslip_list_by_month")
]
