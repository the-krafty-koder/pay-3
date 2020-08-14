import datetime
import pytz

from django.db import models
from django.utils import timezone

from functools import reduce
from picklefield.fields import PickledObjectField

from employee_management.models import Employee

from .exception import ObjectsNotValidatedError


class Attendance(models.Model):
    """
      Attendance model
    """
    employee = models.ForeignKey(
       Employee,
       on_delete=models.CASCADE,
       related_name="employee_attendance",
    )
    name = models.CharField(max_length=20, null=True)
    date_created = models.DateField(auto_now_add=True)
    check_in_toggle = models.BooleanField(default=False)
    check_in_time = models.DateTimeField(null=True, default=None)
    check_out_time = models.DateTimeField(null=True, default=None)
    in_time = models.DateTimeField(null=True, default=None)
    out_time = models.DateTimeField(null=True, default=None)
    is_late = models.BooleanField(default=False)

    def update_checkin_toggle(self):
        """
            Toggles check in object
        """
        if self.check_in_toggle:
            self.out_time = timezone.now()
            self.check_in_toggle = False
        else:
            if self.check_in_time is None:
                self.check_in_time = timezone.now()
                if timezone.now().time().hour > 9:
                    self.is_late = True
            self.in_time = timezone.now()
            self.check_in_toggle = True
        self.save()

    def update_checkout(self):
        """
            Updates check out time to last out time
        """
        self.check_out_time = self.out_time
        self.check_in_toggle = False

    def __str__(self):
        return f"{self.employee.full_name}-Attendance-{self.date_created.__str__()}"

    def save(self, *args, **kwargs):
        self.name = self.__str__()
        super(Attendance, self).save(*args, **kwargs)


class DailyAttendanceManager(models.Manager):

    def create(self, **obj_data):
        return super().create(**obj_data)


class DailyAttendance(models.Model):

    date_created = models.DateField(auto_now=True)
    employee_attendance_objects = PickledObjectField(default=dict)
    status = models.CharField(max_length=4, default=None, null=True)
    name = models.CharField(max_length=15, null=True)
    firm = models.CharField(max_length=50, null=True)

    def update_checkout(self):
        """
           Updates checkout time with last employee checkout,returns employees
           not checked out if any.
        """

        all_out = {}
        for obj, value in self.employee_attendance_objects.items():
            if value.check_in_toggle is False:
                all_out.update({obj: (True)})
            else:
                all_out.update({obj: (False)})

        if reduce(lambda a, b: b is True, all_out.values()):
            for obj, value in self.employee_attendance_objects.items():
                value.update_checkout()
            self.save()
        else:
            invalid = dict(
                    filter(lambda elem: elem[1] is not True, all_out.items())).keys()
            raise ObjectsNotValidatedError(not_validated=invalid)

    def update_last_checkout(self):
        """
           Updates employees not checked out checkout time with last employee
           checkout.
        """
        all_out = {}
        for obj, value in self.employee_attendance_objects.items():
            if value.check_in_toggle is False:
                all_out.update({obj: (True)})
            else:
                all_out.update({obj: (False)})

        not_checked_out = dict(filter(lambda elem: elem[1] is not True,
                                      all_out.items())
                               )
        for key in not_checked_out:
            self.employee_attendance_objects.get(key).update_checkout()
        self.save()

    def save(self, *args, **kwargs):
        if self.status is None:
            self.employee_attendance_objects = {}

            for employee in Employee.objects.all():
                self.employee_attendance_objects.update(
                 {f"{employee.full_name}": Attendance.objects.create(
                                                            employee=employee)
                  })

            self.name = f"Attendance Records for  Date {self.date_created}"
            self.status = "Done"

        super(DailyAttendance, self).save(*args, **kwargs)
