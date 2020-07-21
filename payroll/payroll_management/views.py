import ast

from urllib.parse import urlencode
from xhtml2pdf import pisa

from django.template.loader import get_template
from django.template import Context
from django.shortcuts import render,HttpResponse,redirect
from django.urls import reverse

from employee_management.builder import EmployeeBuilder
from employee_management.models import *
from employee_management.forms import SearchForm

from .forms import *
from .builder import PaySlipBuilder


# Create your views here.

def commit(form,name):
    saved = form.save(commit=False)
    saved.employee = name
    saved.save()
    return saved

def convert_to_dict(series):
    result = {}
    for key in series:result.update({key["name"]:key["amount"]})
    return result

def return_encoded(calculations,type,form):
    """
        Return an encoded url string
    """
    if type == "ca":
        calculations["custom_allowance"].append({"name":form.name,"amount":form.amount})
        return urlencode(calculations),calculations
    else:
        calculations["custom_deduction"].append({"name":form.name,"amount":form.amount})
    return urlencode(calculations),calculations



def create_payslip(request,employee_firstname,employee_lastname,payslip_name=None):

    employee = EmployeeBuilder.get_employee_static("{} {}".format(employee_firstname,employee_lastname))
    custom_allowance = ast.literal_eval(request.GET.get("custom_allowance","[]"))
    custom_deduction = ast.literal_eval(request.GET.get("custom_deduction","[]"))

    if payslip_name !=None:
        payslip = PaySlipBuilder.get_payslip_static(payslip_name)
    else:
        payslip = PaySlipBuilder(employee).create_payslip()

    def return_encoded_string(custom_type=None):
        encoded_string,calculations = return_encoded(
                                                     {"custom_allowance":custom_allowance,
                                                      "custom_deduction":custom_deduction},
                                                      custom_type,saved
                                                    )

        PaySlipBuilder(employee).edit_payslip(payslip.name,
                                              convert_to_dict(calculations["custom_allowance"]),
                                              convert_to_dict(calculations["custom_deduction"])
                                             )

        return encoded_string

    if request.method=="POST":

        addition_form = CustomAllowanceForm(request.POST)
        deduction_form = CustomDeductionForm(request.POST)
        form = PaySlipForm(request.POST,instance=payslip,type="post")

        if "addition_button" in request.POST:

            if addition_form.is_valid() :
                saved = commit(addition_form,employee.full_name)
                encoded_string = return_encoded_string("ca")
                return redirect(f'/payslip/create_payslip/{employee_firstname}/{employee_lastname}/{payslip.name}/?{encoded_string}')
            else:
                return HttpResponse(form.errors)

        if "deduction_button" in request.POST:

            if deduction_form.is_valid():
                saved = commit(deduction_form,employee.full_name)
                encoded_string = return_encoded_string()
                return redirect(f'/payslip/create_payslip/{employee_firstname}/{employee_lastname}/{payslip.name}/?{encoded_string}')

            else:
                return HttpResponse(form.errors)

        if "final_button" in request.POST:
            if form.is_valid():
                PaySlipBuilder.delete_second_last()
                form.save()
                return redirect('payslip_review',employee_firstname=employee.first_name,
                                employee_lastname=employee.last_name,payslip_name=payslip.name
                       )
            else:
                return HttpResponse(form.errors)

    else:
        form = PaySlipForm(instance=payslip,type="initial",initial={"all_allowances":payslip.all_allowances})
        addition_form = CustomAllowanceForm()
        deduction_form = CustomDeductionForm()

    return render(request,"create_payslip.html",
                  {"form":form,"addition_form":addition_form,
                  "deduction_form":deduction_form,"custom_allowance":custom_allowance,
                  "custom_deduction":custom_deduction,
                  "initial_allowances":payslip.all_allowances
                  })

def review_payslip(request,employee_firstname,employee_lastname,payslip_name):

    employee = EmployeeBuilder.get_employee_static("{} {}".format(employee_firstname,employee_lastname))
    payslip = PaySlipBuilder.get_payslip_static(payslip_name)

    return render(request,"review_payslip.html",{"form":payslip})

def list_payslips(request,employee_name=None):

    if employee_name != None:
        payslip_list = PaySlipBuilder.list_payslips_employee(employee_name)
    else:
        payslip_list = PaySlipBuilder.list_payslips()

    if request.method=="POST":
        form = SearchForm(request.POST)

        if form.is_valid():
            employee_text = form.cleaned_data["search_text"]
            return redirect('payslips_list',employee_name=employee_text)
        else:
            return HttpResponse(form.errors)
    else:
        form = SearchForm()

    return render(request,"list_payslips.html",{"payslip_list":payslip_list,"form":form})

def dashboard_payroll(request):
    slips = PaySlip.objects.all()
    employees = Employee.objects.all()
    allowances,deductions = sum((slip.total_allowances for slip in slips)), sum((slip.total_deductions for slip in slips))
    payslips = PaySlip.objects.all().order_by("date_created")[:15]
    num = Firm.objects.get(firm_name="Jos Org").get_number_employees()
    context = {"payslips":payslips,"allowances":allowances,"deductions":deductions,"num":num,"employees":employees}

    return render(request,"payroll_dashboard.html",context)

def delete_payslip(request,payslip_name):
    """
        Deletes an employee from the database then redirects back to employee list
    """

    deleted_payslip = PaySlipBuilder.delete_payslip(payslip_name)
    return redirect('dashboard_payroll')

def render_pdf_view(request,payslip_name):
    payslip = PaySlipBuilder.get_payslip_static(payslip_name)

    template_path = 'payslip_template.html'
    company_name = request.user.firm_name
    phone_number = payslip.employee.phone_number
    email = payslip.employee.email
    context = {"payslip":payslip,"company_name":company_name,"email":email,"phone_number":phone_number}

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename={payslip_name}.pdf'

    template = get_template(template_path)
    html = template.render(context)


    pisaStatus = pisa.CreatePDF(
       html, dest=response)

    if pisaStatus.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response
