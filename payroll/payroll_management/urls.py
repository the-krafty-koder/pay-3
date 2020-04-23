from django.urls import path,include,re_path
from .views import *

urlpatterns = [
    path('create_payslip/<str:employee_firstname>/<str:employee_lastname>', create_payslip,name="payslip_create"),
    #re_path(r'^create_payslip/(?P<employee_firstname>\w+)/(?P<employee_lastname>\w+)/$',create_payslip,name="payslip_create"),
    re_path(r'^create_payslip/(?P<employee_firstname>\w+)/(?P<employee_lastname>\w+)/(?P<payslip_name>\w+)/$',create_payslip,name="payslip_create"),
    path('review_payslip/<str:employee_firstname>/<str:employee_lastname>/<str:payslip_name>', review_payslip,name="payslip_review"),
    path('list_payslips',list_payslips, name="payslips_list"),
    path('list_payslips/<str:employee_name>', list_payslips,name="payslips_list"),
    path('delete_payslip/<str:payslip_name>',delete_payslip, name="payslip_delete"),
    path('dashboard_payroll',dashboard_payroll, name="dashboard_payroll"),
    path('download_payslip/<str:payslip_name>',render_pdf_view,name="download_payslip"),
]
#(?P<custom_allowance>\w+|)/?:(?P<custom_deduction>\w+)
