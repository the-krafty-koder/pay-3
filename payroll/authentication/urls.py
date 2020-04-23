from django.urls import path,include
from .views import *

urlpatterns = [
    path('login', loginto,name="login"),
    path('login/<str:invalid>', loginto,name="login"),
    path('signup', signup,name="signup"),
    path('create_firm', create_firm,name="create_firm"),
    path('logout', logout_view,name="logout"),
    path('employee_login', employee_login,name="employee_login"),

]
