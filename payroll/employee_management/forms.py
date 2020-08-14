from django import forms
from django.forms import ModelForm
from .models import *

level_choice_fields = [
    ('Full-time', 'Full Time',),
    ('Part-time', 'Part Time'),
    ('Fixed-term', 'Fixed Term')
]
gender_choice_fields = [
    ('Male', 'Male',),
    ('Female', 'Female'),
    ('Other', 'Other')
]


class EmployeeForm(ModelForm):
    gender = forms.ChoiceField(choices=gender_choice_fields)

    def __init__(self, *args, **kwargs):
        contract = kwargs.pop("contract", None)
        if contract is not None:

            kwargs.update(initial={"start_date": contract.start_date,
                                   "end_date": contract.end_date,
                                   "contract_type": contract.contract_type,
                                   "base_salary": contract.base_salary})
        super(EmployeeForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Employee
        widgets = {
            "nhif_number": forms.Textarea(attrs={'rows': 1, 'cols': 20}),
            "nssf_number": forms.Textarea(attrs={'rows': 1, 'cols': 20}),
            "kra_pin": forms.Textarea(attrs={'rows': 1, 'cols': 20}),
            "home_address": forms.Textarea(attrs={'rows': 1, 'cols': 20}),
        }
        exclude = ["contract", "firm", "full_name"]


class EducationForm(ModelForm):

    class Meta:
        model = Education
        fields = '__all__'


class DocumentForm(ModelForm):

    class Meta:
        model = Document
        fields = '__all__'


class EditEmployeeForm(ModelForm):

    class Meta:
        model = Employee
        widgets = {
            "nhif_number": forms.Textarea(attrs={'rows': 1, 'cols': 20}),
            "nssf_number": forms.Textarea(attrs={'rows': 1, 'cols': 20}),
            "kra_pin": forms.Textarea(attrs={'rows': 1, 'cols': 20}),
            "home_address": forms.Textarea(attrs={'rows': 1, 'cols': 20})
        }
        exclude = ["firm", "full_name"]


class ContractForm(ModelForm):
    contract_type = forms.ChoiceField(choices=level_choice_fields)

    class Meta:
        model = Contract
        exclude = ["allowances"]


class SearchForm(forms.Form):

    search_text = forms.CharField()


class FirmProfileForm(ModelForm):

    class Meta:
        model = FirmProfile
        fields = "__all__"
        widgets = {
            "mailing_address": forms.Textarea(attrs={'rows': 1, 'cols': 20})
        }

class EditFirmProfileForm(ModelForm):

    class Meta:
        model = FirmProfile
        fields = "__all__"
        widgets = {
            "mailing_address": forms.Textarea(attrs={'rows': 1, 'cols': 20})
        }
