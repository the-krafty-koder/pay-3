from django import forms
from django.forms import ModelForm

from .models import PaySlip,CustomAllowance,CustomDeduction
from picklefield.fields import PickledObjectField

class PaySlipForm(ModelForm):
    nhif = forms.IntegerField()
    nssf = forms.IntegerField()
    total_deductions = forms.FloatField()
    total_allowances = forms.FloatField()

    all_allowances = PickledObjectField()

    taxable = forms.FloatField()
    relief = forms.FloatField()
    tax_charged = forms.FloatField()
    paye = forms.FloatField()

    basic_salary = forms.FloatField()
    net_salary = forms.FloatField()
    gross_salary = forms.FloatField()

    def __init__(self,*args,**kwargs):
        request_type = kwargs.pop("type",None)
        if request_type == "initial":
            payslip = kwargs.get("instance",None)
            #deductions = list(payslip.all_deductions.values())

            kwargs.update(initial={"gross_salary":payslip.gross_salary,"net_salary":payslip.net_salary,
                                    "basic":payslip.basic_salary,"nhif":payslip.nhif,"nssf":payslip.nssf,
                                    "total_deductions":payslip.get_total_deductions,"tax_charged":payslip.tax_charged,"paye":payslip.paye,"total_allowances":payslip.get_total_allowances,
                                    "relief":payslip.relief,"taxable":payslip.taxable,
                                  })

        super(PaySlipForm,self).__init__(*args,**kwargs)


    class Meta:
        model = PaySlip

        exclude = ["name","editable"]

class CustomAllowanceForm(ModelForm):

    class Meta:
        model = CustomAllowance
        exclude = ["employee"]

class CustomDeductionForm(ModelForm):

    class Meta:
        model = CustomDeduction
        exclude = ["employee"]
