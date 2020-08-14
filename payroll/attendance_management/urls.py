from django.urls import path,include
from .views import (
    create_daily_attendance,
    list_attendance,
    DailyAttendanceListview,
    attendance_dashboard,
    employee_check_in,
    check_in_declined,
    employee_checkin_toggle,
    find_employee_ip,
    validate,
    find_employee_ip
)


urlpatterns = [
    path('create_attendance', create_daily_attendance, name='attendance_create'),
    path('list_attendance', list_attendance, name='attendance_list'),
    path('list_attendance/<str:date>', list_attendance, name='attendance_list'),
    path('list_records', DailyAttendanceListview.as_view(), name='attendance_records'),
    path('list_records/<str:date>', DailyAttendanceListview.as_view(), name='attendance_records'),
    path('dashboard_attendance', attendance_dashboard, name='attendance_dashboard'),
    path('employee_check_in/<str:employee_name>', employee_check_in, name='check_in_employee'),
    path('employee_check_in/declined', check_in_declined, name='check_in_declined'),
    path('employee_checkin_toggle/<str:employee_name>', employee_checkin_toggle, name='toggle_employee'),
    path('find_ip/<str:employee_name>', find_employee_ip, name='ip_employee'),
    path('validate/<str:employee_name>', validate, name='ip'),
    path('find_ip/<str:longitude>/<str:latitude>/<str:employee_name>', find_employee_ip, name='ip_employee'),

]
