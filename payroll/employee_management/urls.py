from django.urls import path,include,re_path
from .views import *


urlpatterns = [
    path('create', create_employee,name="employee_create"),
    path('create/<str:employee_name>', create_employee,name="create_within"),
    path('edit/<str:employee_firstname>/<str:employee_lastname>', edit_employee,name="edit_employee"),
    path('list/', list_employees,name="employee_list"),
    path('list/<str:employee_name>', list_employees,name="employee_list"),
    path('add_employee_documents/<str:employee_name>', add_employee_documents,name="documents_add"),
    path('create_contract/<str:employee_firstname>/<str:employee_lastname>', create_employee_contract,name="contract_create"),
    re_path(r'^create_contract/(?P<employee_firstname>\w+)/(?P<employee_lastname>\w+)/$',create_employee_contract,name="contract_create"),
    path('delete/<str:employee_firstname>/<str:employee_lastname>',delete_employee, name="employee_delete"),
    path('profile/<str:employee_firstname>/<str:employee_lastname>', profile_employee,name="employee_profile"),
    path('list/search/<str:employee_firstname>/<str:employee_lastname>', search_employee,name="employee_search"),
]
