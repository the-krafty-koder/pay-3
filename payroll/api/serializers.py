from rest_framework import serializers
from employee_management.models import Employee
from payroll_management.models import PaySlip


class EmployeeSerializer(serializers.ModelSerializer):
    """
        Serializer for Employee model
    """

    class Meta(object):
        model = Employee
        fields = "__all__"


class PaySlipSerializer(serializers.ModelSerializer):
    """
        Serializer for PaySlip model
    """

    class Meta(object):
        model = PaySlip
        fields = "__all__"
