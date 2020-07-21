from django.db import models
from django.db import transaction

from employee_management.models import *

from .calculations import *

# Create your models here.

class CustomAllowance(models.Model):
    employee = models.CharField(max_length=40,null=True)
    name = models.CharField(max_length=40)
    amount = models.FloatField()


class CustomDeduction(models.Model):
    employee = models.CharField(max_length=40,null=True)
    name = models.CharField(max_length=40)
    amount = models.FloatField()

    def save(self,*args,**kwargs):
        self.amount = -self.amount
        super(CustomDeduction,self).save(*args,**kwargs)

class PaySlipManager(models.Manager):

    def create(self,**obj_data):

        self.model.all_allowances = obj_data.get("employee").contract.allowances
        return super().create(**obj_data)


class PaySlip(models.Model):
    name = models.CharField(max_length=50)
    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name="employee_payslip",
    )
    date_created = models.DateTimeField(auto_now_add=False,null=True)
    editable = models.BooleanField()

    objects = PaySlipManager()

    status = PickledObjectField(null=True,default="Update")

    all_allowances = PickledObjectField(null=True)
    all_deductions = PickledObjectField(null=True,default=dict)
    all_taxation = PickledObjectField(null=True,default=dict) # a dictionary of calculation values
    total_allowances = models.FloatField(default=0)
    total_deductions = models.FloatField(default=0)

    net_salary = models.FloatField(default=0)
    gross_salary = models.FloatField(default=0)
    relief = models.FloatField(default=0)
    taxable = models.FloatField(default=0)
    basic_salary = models.FloatField(default=0)
    nssf = models.FloatField(default=0)
    nhif = models.FloatField(default=0)
    paye = models.FloatField(default=0)
    tax_charged = models.FloatField(default=0,null=True)

    """
    class Meta:
        private_fields = ('net_salary','gross_salary','relief','taxable','basic_salary','nssf','nhif','total_deductions','total_allowances','all_allowances','all_deductions','all_taxation')
    """
    @property
    def total_taxation(self):
        return self.total_taxation

    @property
    def get_total_allowances(self):
        return self.total_allowances

    @property
    def get_total_deductions(self):
        return self.total_deductions

    @property
    def get_all_taxation(self):
        pass

    @property
    def get_all_allowances(self):
        return self.all_allowances

    @property
    def get_all_deductions(self):
        return self.all_deductions

    @property
    def get_all_taxation(self):
        return self.all_taxation


    def set_all_deductions(self,new_deduct):
        self.update_calculations(deductions=new_deduct)

    def set_all_allowances(self,new_allowances):
        self.update_calculations(allowances=new_allowances)

    #def set_all_taxation(self,new_taxes=None):
        #self.all_taxation = new_taxes

    def update_calculations(self,allowances={},deductions={},admissible={},basic=None):

        if allowances == {}:
            allowances = self.all_allowances
        if deductions == {}:
            deductions = self.all_deductions
        if admissible == {}:
            admissible = {"NSSF":self.nssf}


        if basic != None:
            calculator = PaySlipCalculator(basic,allowances)
            self.basic_salary = basic
        else:
            calculator = PaySlipCalculator(self.basic_salary,allowances,deductions,admissible)

        self.all_deductions = calculator.get_deductions()
        self.all_taxation = calculator.get_taxation()
        self.all_allowances = calculator.get_allowances()
        self.relief = calculator.get_relief()
        self.net_salary = calculator.get_net_salary()
        self.gross_salary = calculator.get_gross()
        self.taxable = calculator.get_taxable()
        self.nssf = calculator.getNSSF()
        self.nhif = calculator.getNHIF()
        self.tax_charged,self.paye = calculator.getPAYE()

    def __str__(self):
        return self.name

    def save(self,*args,**kwargs):
        if self.status == "Update":
            basic_salary = self.employee.contract.base_salary
            self.all_allowances = self.employee.contract.allowances
            self.update_calculations(basic=basic_salary,allowances=self.employee.contract.allowances)
            self.status = "AfterUpdate"

        self.total_allowances = sum(self.all_allowances.values())
        self.total_deductions = sum(self.all_deductions.values())


        super(PaySlip,self).save(*args,**kwargs)
