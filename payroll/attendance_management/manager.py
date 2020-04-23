from .models import *

class AttendanceManager(object):
    """Manages the Attendance object"""

    def __init__(self,dailyattendance):
        self.daily_attendance = dailyattendance
        self.attendance_records = dailyattendance.employee_attendance_objects

    def toggle_attendance_object(self,employee_name):
        attendance_object = self.daily_attendance.employee_attendance_objects.get(employee_name)
        attendance_object.update_checkin_toggle()
        self.daily_attendance.save()

    def check_attendance_object(self,employee_name):
        attendance_object = self.daily_attendance.employee_attendance_objects.get(employee_name)
        return attendance_object.check_in_toggle

    def submit_final_attendance(self):
        try :
            self.daily_attendance.update_checkout()
            return True
        except ObjectsNotValidatedError as e:
            return e.__str__().split(":")[1]

    def submit_last_checkout(self):
        self.daily_attendance.update_last_checkout()
        self.daily_attendance.save()

class AttendanceBuilder():

    @staticmethod
    def create_attendance():
        if DailyAttendance.objects.filter(date_created=timezone.localdate())==[]:
            return DailyAttendance.objects.create()

    @staticmethod
    def get_attendance():
        return DailyAttendance.objects.filter(date_created=timezone.localdate())[0]
