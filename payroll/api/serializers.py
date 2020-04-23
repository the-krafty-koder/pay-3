from rest_framework import serializers
from employee_management.models import *
from payroll_management.models import *


class EmployeeSerializer(serializers.ModelSerializer):

    class Meta(object):
        model = Employee
        fields = "__all__"

class PaySlipSerializer(serializers.ModelSerializer):

    class Meta(object):
        model = PaySlip
        fields = "__all__"
