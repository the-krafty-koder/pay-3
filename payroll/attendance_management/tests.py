from django.test import TestCase
from .models import *

# Create your tests here.
class TestDailyAttendanceCreation(TestCase):

    def setUp(self):
        self.att = DailyAttendance.objects.create()
    def testIfCreated(self):
        #self.assertEqual(self.att.status,"Done")
        pass

    def testIfCheckInToggleUpdated(self):
        self.assertEqual(self.att.status,"Done")
        obj = self.att.employee_attendance_objects["Juma Mukosi"]
        obj.update_checkin_toggle()
        self.assertEqual(len(self.att.employee_attendance_objects.values()),4)
        self.assertNotEqual(obj.in_time,None)

    def testIfDailyAttendanceSubmitted(self):
        pass
