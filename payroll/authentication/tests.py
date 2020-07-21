
import requests
from datetime import datetime as date
from django.test import TestCase
from .models import UserEmployee
from employee_management.models import Firm,Employee,Contract

from .mail import send_login_mail
"""

# Create your tests here.
def setUp(self):

    self.new_employee = UserEmployee.objects.create_employee("Omollo Otis",
                                                             "omootis@gmail.com",
                                                             "Nation Digitalz",
                                                             "omootis254")

class TestEmployeeCreation(TestCase):

    def setUp(self):
        self.firm = Firm.objects.create(firm_name="Mater Company",email="mter@gmail.com",address="675,Nairobi")
        self.new_employee = UserEmployee.objects.create_employee(
            "Omollo Otis",
            "omootis@gmail.com",
            self.firm.firm_name,
            "omootis254"
        )

    def testIfEmployeeCreated(self):
        created_employee = UserEmployee.objects.get(name="Omollo Otis")
        self.assertTrue(created_employee.name,self.new_employee.name)

    def testIfEmployeeCreatedAsAdmin(self):
        self.assertFalse(self.new_employee.is_admin,True)


class TestIfMailSent(TestCase):

    def setUp(self):
        self.new_employee = Employee.objects.create(
            first_name="Omo",
            last_name="Ous",
            home_address="57, Kisumu",
            phone_number="0712345678",
            email="me@gmail.com",
            kra_pin="453547",
            nhif_number="543564",
            nssf_number="653473",
            department="Sales",
            is_manager=False,
            contract = Contract.objects.create(start_date=date.now(),end_date=date.now(),contract_type="Permanent",base_salary=45000.00),
            firm = Firm.objects.create(firm_name="Sun Systems",address="53, Kisumu")
        )

    
    def test_mail_response_status_code(self):
        response = send_login_mail("Omoga Omondi","omondio254@gmail.com","Freelancer","GHEYGVDHEUYJUEYEGJ")
        self.assertEqual(response,True)

    def test_if_user_employee_object_created(self):
        self.assertEqual(Employee.objects.filter(full_name=self.new_employee.full_name).count(),1)
        self.assertEqual(UserEmployee.objects.filter(name=self.new_employee.full_name).count(),1)
"""
from .views import get_logged_in_user

class TestUser(TestCase):
    """docstring for TestUser"""
    
    def test_get_logged_in_user(self):
        self.assertEqual(requests.get("http://127.0.0.1:8000/authentication/logged_in_user").text,"Mater Company")
