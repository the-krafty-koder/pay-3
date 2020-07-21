import datetime,calendar

from django.utils.dates import MONTHS

from employee_management.builder import EmployeeBuilder

from .models import PaySlip
from .calculations import *


def return_payslip_list(queryset):
    payslip_list =  {month:[slip for slip in queryset if calendar.month_name[slip.date_created.month]==month] for month in MONTHS.values()}
    return dict(filter(lambda elem: elem[1] != [],payslip_list.items()))

class PaySlipBuilder:

    def __init__(self,employee):
        self.employee = employee

    @staticmethod
    def delete_payslip(name):
        PaySlip.objects.filter(name=name).delete()

    @staticmethod
    def get_payslip_static(name):
        return PaySlip.objects.get(name=name)

    def get_payslip(self,name):
        return PaySlip.objects.get(name=name)

    @staticmethod
    def list_payslips():
        return return_payslip_list(PaySlip.objects.all())

    @staticmethod
    def delete_second_last():
        d = list(PaySlip.objects.all())[-2]
        d.delete()

    @staticmethod
    def list_payslips_employee(employee_name):
        payslip_queryset = PaySlip.objects.filter(employee=EmployeeBuilder.get_employee_static(employee_name))
        return return_payslip_list(payslip_queryset)

    def create_payslip(self):
        today = datetime.datetime.now().date()
        index = PaySlip.objects.filter(employee=self.employee).__len__()
        payslip_name = "Employee_{0}_Payslip_{1}".format(self.employee.full_name.replace(" ",""),index)
        return PaySlip.objects.create(name=payslip_name,employee=self.employee, date_created=today,editable=True)
        #return payslip_name

    def edit_payslip(self,payslip_name,new_allowances,new_deductions):
        payslip = self.get_payslip(payslip_name)
        initial_allowances = payslip.all_allowances
        new_allowances.update(initial_allowances)

        if new_allowances:
            payslip.set_all_allowances(new_allowances)
            payslip.save()


        if new_deductions:
            payslip.set_all_deductions(new_deductions)
            payslip.save()
            return payslip
