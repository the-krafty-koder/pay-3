from django.utils import timezone
from .models import DailyAttendance
from .exception import ObjectsNotValidatedError


class AttendanceManager(object):
    """Manages the Attendance object"""

    def __init__(self,dailyattendance):
        self.daily_attendance = dailyattendance
        self.attendance_records = dailyattendance.employee_attendance_objects

    def toggle_attendance_object(self,employee_name):
        """
            Toggles attendance between checked in and checked out
        """
        attendance_object = self.daily_attendance.employee_attendance_objects.get(employee_name)
        attendance_object.update_checkin_toggle()
        self.daily_attendance.save()

    def check_attendance_object(self, employee_name):
        """
            Checks current state of attendance object
        """
        attendance_object = self.daily_attendance.employee_attendance_objects.get(employee_name)
        return attendance_object.check_in_toggle

    def submit_final_attendance(self):
        """
            Submits final end of day attendance of all objects
        """
        try:
            self.daily_attendance.update_checkout()
            return True
        except ObjectsNotValidatedError as e:
            return e.__str__().split(":")[1]

    def submit_last_checkout(self):
        """
            Submits  day attendance using state of last checkout
        """
        self.daily_attendance.update_last_checkout()
        self.daily_attendance.save()


class AttendanceBuilder():

    @staticmethod
    def create_attendance():
        """
            Creates attendance object
        """
        if not DailyAttendance.objects.filter(date_created=timezone.localdate()):
            return DailyAttendance.objects.create()

    @staticmethod
    def get_attendance():
        """
            Returns attendance object
        """
        return DailyAttendance.objects.filter(date_created=timezone.localdate()).first()
