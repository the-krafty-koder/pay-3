import datetime

from django.test import TestCase

from .models import *
from .builder import EmployeeBuilder

# Create your tests here.

class TestEmployee(TestCase):

    def setUp(self):
        pass

    def testEmployeeCreate(self):
        """
            Test if employee object is created,employee is retrieved and full name is added
            to the database.s

        """
        new_employee = Employee.objects.create(
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
        self.assertTrue(new_employee)
        self.assertTrue(Employee.objects.get(first_name="Omo"))
        self.assertEqual(Employee.objects.get(first_name="Omo").full_name,"Omo Ous")

    def testEmployeeRetrieve(self):
        pass



    def testEmployeeInvalidNumber(self):
        """
            Test if phone number validator works

        """
        new_employee = Employee.objects.create(
            first_name="Otieno",
            last_name="Ousa",
            home_address="57, Kisumu",
            phone_number="+25471",
            email="me@gmail.com",
            kra_pin="453547",
            nhif_number="543564",
            nssf_number="653473",
            department="Sales",
            is_manager=False,
            contract = Contract.objects.create(start_date=date.now(),end_date=date.now(),contract_type="Permanent",base_salary=45000.00),
            firm = Firm.objects.create(firm_name="Sun Systems",address="53, Kisumu")
        )
        self.assertEqual(new_employee.phone_number,"+25471")

    def testEmployeeInvalidEmail(self):
        """
            Test if email validator works

        """
        new_employee = Employee.objects.create(
            first_name="Otieno",
            last_name="Ousadi",
            home_address="57, Kisumu",
            phone_number="+25471",
            email="megmail.com",
            kra_pin="453547",
            nhif_number="543564",
            nssf_number="653473",
            department="Sales",
            is_manager=False,
            contract = Contract.objects.create(start_date=date.now(),end_date=date.now(),contract_type="Permanent",base_salary=45000.00),
            firm = Firm.objects.create(firm_name="Sun Systems",address="53, Kisumu")
        )
        self.assertEqual(new_employee.email,"megmail.com")

    def testEmployeeDelete(self):
        new_employee = Employee.objects.create(
            first_name="Omollo",
            last_name="Otiende",
            home_address="57, Kisumu",
            phone_number="+25471",
            email="megmail.com",
            kra_pin="453547",
            nhif_number="543564",
            nssf_number="653473",
            department="Sales",
            is_manager=False,
            contract = Contract.objects.create(start_date=date.now(),end_date=date.now(),contract_type="Permanent",base_salary=45000.00),
            firm = Firm.objects.create(firm_name="Sun Systems",address="53, Kisumu")
        )
        EmployeeBuilder("Omollo Otiende").delete()
        self.assertFalse(Employee.objects.get(full_name="Omollo Otiende")

    def testEmployeeSearch(self):
        pass
