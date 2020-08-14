from django import forms
from django.forms import ModelForm
from .models import Firm

class login_form(forms.Form):

    name = forms.CharField(max_length=45)
    company_name = forms.CharField(max_length=50)
    attrs = {
        "type": "password"
    }

    password = forms.CharField(min_length=8, widget=forms.TextInput(attrs=attrs))


class signup_form(forms.Form):
    user_name = forms.CharField(max_length=45)
    email = forms.EmailField()
    company_name = forms.CharField(max_length=45)
    attrs = {
        "type": "password"
    }
    password = forms.CharField(min_length=8, widget=forms.TextInput(attrs=attrs))


class firm_form(ModelForm):
    class Meta:
        model = Firm
        widgets = {
            "address": forms.Textarea(attrs={'rows': 1, 'cols': 20})
        }
        exclude = ["firm_profile"]
