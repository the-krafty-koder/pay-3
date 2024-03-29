"""payroll URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from employee_management.views import create_employee
from .views import *

urlpatterns = [
    path('', create_employee, name='landing'),
    path('admin/', admin.site.urls),
    path('employee/', include('employee_management.urls')),
    path('payslip/', include('payroll_management.urls')),
    path('authentication/', include('authentication.urls')),
    path('attendance/', include('attendance_management.urls')),
    path('api/', include('api.urls')),
    path('firm_profile',firm_profile,name="profile_firm"),
    path('firm_profile_create', create_firm_profile,name="profile_firm_create"),
    path('firm_profile_edit', edit_firm_profile,name="profile_firm_edit"),
    path('firm_profile_view', view_firm_profile,name="profile_firm_view"),

]

urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)
