import json,ast

from django.core import serializers
from django.shortcuts import render,HttpResponse,redirect
from django.views.generic.edit import FormView

from payroll_management.forms import CustomAllowanceForm
from payroll_management.views import return_encoded

from .forms import *
from .builder import EmployeeBuilder


def create_employee(request,employee_name=None):
    """
        Loads view to create an employee
    """
    employee = None
    
    if employee_name != None:
            employee = EmployeeBuilder.get_employee_static(employee_name)

    if request.method=="POST":
        form = EmployeeForm(request.POST,request.FILES)
        

        if employee != None:
            form = EmployeeForm(request.POST,request.FILES,instance=employee)

        if "form_button" in request.POST:
            if form.is_valid():
                form_clean = form.cleaned_data
                UploadedImage.objects.create(employee=f"{form_clean['first_name']} {form_clean['last_name']}",
                                             image=request.FILES['image'])
                del form_clean['image']
                request.session["new_user_personal"] = form_clean
                return redirect('contract_create',
                                employee_firstname=form_clean['first_name'],
                                employee_lastname=form_clean['last_name'])

    else:
        if employee!=None:
            form = EmployeeForm(instance=employee,contract=employee.contract)
        else:
            form = EmployeeForm()
            education_form,document_form = EducationForm(), DocumentForm()
            education,documents= None,None

    return render(request,"create_employee.html",{"form":form,
                                                  "document_form":document_form,
                                                  "education_form":education_form,
                                                  "employee":employee,
                                                  "education":education,
                                                  "documents":documents})

def add_employee_documents(request,employee_name):
    employee = EmployeeBuilder.get_employee_static(employee_name)

    if request.method=="POST":
        education_form = EducationForm(request.POST,request.FILES)
        document_form = DocumentForm(request.POST,request.FILES)

        if "education_button" in request.POST:
            if education_form.is_valid():
                education_form = education_form.save()
                employee.education.append(education_form)
                employee.save()
                return redirect('documents_add',employee_name=education_form.employee)
            else:
                return HttpResponse(form.errors)

        if "document_button" in request.POST:
            if document_form.is_valid():
                document_form = document_form.save()
                employee.documents.append(document_form)
                employee.save()
                return redirect('documents_add',employee_name=document_form.employee)
            else:
                return HttpResponse(form.errors)

    else:
        education_form,document_form = EducationForm(initial={"employee":employee}),DocumentForm(initial={"employee":employee})

        education,documents = Education.objects.filter(employee=employee.full_name),Document.objects.filter(employee=employee.full_name)

    return render(request,"add_employee_documents.html",{"document_form":document_form,
                                                         "education_form":education_form,
                                                         "employee":employee,
                                                         "education":education,
                                                         "documents":documents}
                  )

def create_employee_contract(request,employee_firstname=None,employee_lastname=None):
    custom_allowance = ast.literal_eval(request.GET.get("custom_allowance","[]"))
    employee_name = f"{employee_firstname} {employee_lastname}"

    try:
        contract = Contract.objects.get(employee_name=employee_name)
    except Exception:
        contract = Contract.objects.create(employee_name=employee_name,contract_type="Permanent",base_salary=0)

    if request.method=="POST":
        form = ContractForm(request.POST,instance=contract)
        addition_form = CustomAllowanceForm(request.POST)

        if "addition_button" in request.POST:
            if addition_form.is_valid() :
                saved = addition_form.save(commit=False)
                encoded_string,calculations = return_encoded({"custom_allowance":custom_allowance},"ca",saved)
                contract.allowances = {allowance.get("name"):allowance.get("amount") for allowance in calculations.get("custom_allowance")}
                contract.save()
                return redirect(f'/employee/create_contract/{employee_firstname}/{employee_lastname}/?{encoded_string}')
                #return HttpResponse({convert_to_dict(calculations["custom_allowance"]).values()})
            else:
                return HttpResponse(form.errors)

        if form.is_valid():

            contract = form.save()
            personal_info = request.session["new_user_personal"]
            personal_info['image'] = UploadedImage.objects.filter(employee=f"{personal_info['first_name']} {personal_info['last_name']}").order_by('-id')[0].image
            saved = EmployeeBuilder.create_employee(personal_info,
                                                    contract,
                                                    Firm.objects.get(firm_name=request.user.firm_name))

            return redirect("documents_add",employee_name=employee_name)
        else:
            return HttpResponse(form.errors)
    else:
            #return HttpResponse("{} does not exist".format(employee_name))
        form = ContractForm(instance=contract)
        addition_form = CustomAllowanceForm()

    return render(request,"employee_contract.html",{"form":form,
                                                    "addition_form":addition_form,
                                                    "custom_allowance":custom_allowance}
                  )

def edit_employee(request,employee_firstname,employee_lastname):
    """
        Loads view to edit an employee
    """

    employee = EmployeeBuilder("{} {}".format(employee_firstname,employee_lastname)).get_employee()

    if request.method=="POST":
        form = EditEmployeeForm(request.POST or None,request.FILES,instance=employee)

        if form.is_valid():
            return HttpResponse("Done")
        else:
            return HttpResponse(form.errors)
    else:
        form = EditEmployeeForm(instance=employee)

    return render(request,"edit_employee.html",{"form":form})

def serialize_employee(employee_object):

    data = json.loads(serializers.serialize("json",[employee_object,]))
    return [field["fields"] for field in data]

def list_employees(request,employee_name=None):
    """
        Lists current employees
    """

    if employee_name != None:
        employee = EmployeeBuilder.get_employee_static(employee_name)
        employee_data = serialize_employee(employee)
    else:
        data = json.loads(serializers.serialize("json",Employee.objects.all()))
        employee_data =  [field["fields"] for field in data]

    if request.method=="POST":
        form = SearchForm(request.POST)

        if form.is_valid():
            cd = form.cleaned_data["search_text"]
            return redirect('employee_list',employee_name=cd)
        else:
            return HttpResponse(form.errors)
    else:
        form = SearchForm()

    return render(request,"list_employees.html",{"employees":employee_data,"form":form})

def delete_employee(request,employee_firstname,employee_lastname):
    """
        Deletes an employee from the database then redirects back to employee list
    """

    deleted_employee = EmployeeBuilder("{} {}".format(employee_firstname,employee_lastname)).delete_employee()
    return redirect('employee_list')

def profile_employee(request,employee_firstname,employee_lastname):
    """
        Loads employee profile
    """
    employee = EmployeeBuilder.get_employee_static("{} {}".format(employee_firstname,employee_lastname))
    return render(request,"employee_profile.html",{"employee":employee})

def search_employee(request,employee_firstname,employee_lastname):
    """
        Returns searched employee by name
    """

    result = EmployeeBuilder.list_employees("{} {}".format(employee_firstname,employee_lastname))
    return redirect('list',employee_data=serialize_employee(result))
