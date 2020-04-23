from .models import *
from .forms import *

class EmployeeBuilder:

    def __init__(self,employee_name):
        self.employee_name = employee_name
        self.employee = self.get_employee()


    @staticmethod
    def create_employee(form_object,contract,firm):
        employee = Employee.objects.create(
            first_name=form_object['first_name'],
            last_name=form_object['last_name'],
            home_address=form_object['home_address'],
            phone_number=form_object['phone_number'],
            identification_number = form_object['identification_number'],
            gender = form_object['gender'],
            email=form_object['email'],
            image=form_object['image'],
            kra_pin=form_object['kra_pin'],
            nhif_number=form_object['nhif_number'],
            nssf_number=form_object['nssf_number'],
            department=form_object['department'],
            is_manager=form_object['is_manager'],
            contract = contract,
            firm = firm
        )
        return employee


    @staticmethod
    def list_employees(employee_name):
        return Employee.objects.filter(full_name=employee_name)

    @staticmethod
    def get_employee_static(employee_name):
        return Employee.objects.get(full_name=employee_name)

    def get_employee(self):
        return Employee.objects.get(full_name=self.employee_name)

    def edit_employee(self,post_object):

        try:
            edited_employee = EditEmployeeForm(post_object,instance=self.employee)
            #edited_employee.contract = contract
            edited_employee.save()
        except Exception as e:
            return e.__str__()

    def delete_employee(self):
        self.employee.delete()

    def add_education(self,education_object):
        self.employee.education.add(education_object)

    def remove_education(self,education_object):
        self.employee.education.discard(education_object)
