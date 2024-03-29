from django.urls import (path,
                         include)
from .views import (loginto,
                    create_firm,
                    signup,
                    logout_view,
                    employee_login,
                    get_logged_in_user)

urlpatterns = [
    path('', loginto, name='login_default'),
    path('login', loginto, name="login"),
    path('login/<str:invalid>', loginto, name="login"),
    path('signup', signup, name="signup"),
    path('create_firm', create_firm, name="create_firm"),
    path('logout', logout_view, name="logout"),
    path('employee_login', employee_login, name="employee_login"),
    path('logged_in_user', get_logged_in_user, name="logged_in_user"),

]
