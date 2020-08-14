import datetime

from django.test import TestCase

from employee_management.builder import EmployeeBuilder

from .models import *
from .calculations import *
from .builder import PaySlipBuilder


# Create your tests here.

class TestPayslip(TestCase):

    def setUp(self):
        pass

    def testPayslipCreate(self):
        """
            Test if payslip object is created,employee is retrieved and full name is added
            to the database

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
            contract = Contract.objects.create(contract_type="Permanent",base_salary=45000.00),
            firm = Firm.objects.create(firm_name="Sun Systems",address="53, Kisumu")
        )
        new_payslip = PaySlip.objects.create(employee=new_employee,editable=False)
        self.assertTrue(new_payslip)
        self.assertTrue(new_payslip.employee)
        self.assertEqual(new_payslip.name,"Employee_OmoOus_Payslip_1")


class TestPayslipBuilder(TestCase):

    def setUp(self):
        self.new_employee = Employee.objects.create(
            first_name="Omo",
            last_name="Ous",
            home_address="57, Kisumu",
            phone_number="0712345678",
            email="me@gmail.com",
            kra_pin="45354733",
            nhif_number="54356444",
            nssf_number="65347673",
            department="Sales",
            is_manager=False,
            contract = Contract.objects.create(contract_type="Permanent",
                                               base_salary=20000.00),
            firm = Firm.objects.create(firm_name="Sun System",
                                       address="53, Kisumu")
        )
        self.payslip=PaySlip.objects.create(name="Omo Ous",
                                              employee=self.new_employee,
                                              date_created=datetime.datetime.now().date(),
                                              editable=False)

    def testPayslipBuilderFunction(self):
        slip = PaySlipBuilder(self.new_employee).create_payslip()
        print(slip)

    def testIfAllowancesSetOnSaving(self):
        self.assertEqual(self.payslip.all_allowances,{})

    def testIfTaxationSetOnSaving(self):
        self.assertEqual(self.payslip.all_taxation,{"PAYE":3540.4,"TAXABLE":20000.0})

    def testIfDeductionsSetOnSaving(self):
        self.assertEqual(self.payslip.all_deductions,{"NSSF":-10800,"NHIF":-750})

    def testBeforeAtomicity(self):
        self.assertEqual(self.payslip.status,None)

        calculator = PaySlipCalculator(self.payslip.basic_salary,{"me":4500,"you":8000},{},{})
        self.payslip.all_allowances = calculator.get_allowances()
        self.payslip.gross_salary = calculator.get_gross()

        self.payslip.all_taxation = calculator.get_taxation()
        self.payslip.all_allowances = calculator.get_allowances()
        #self.relief = calculator.get_relief()
        self.payslip.net_salary = calculator.get_net_salary()
        self.payslip.gross_salary = calculator.get_gross()
        self.payslip.taxable = calculator.get_taxable()
        self.payslip.nssf = calculator.getNSSF()
        self.payslip.nhif = calculator.getNHIF()
        self.payslip.editable = True

        self.payslip.save()
        self.assertEqual(self.payslip.all_allowances,{"me":4500.0,"you":8000.0})
        self.assertEqual(self.payslip.gross_salary,32500)

    def testAtomicity(self):
        payslip = PaySlip.objects.get(name="Omo Ous")
        self.assertEqual(payslip.all_allowances,{"me":4500.0,"you":8000.0})
        self.assertEqual(payslip.gross_salary,32500)


class TestCalculations(TestCase):

    def setUp(self):
        self.base = 5000

    def testNHIF(self):
        result = NHIF(self.base).get_value()
        self.assertTrue(result)
        self.assertEqual(result, -150)

    def testNSSF(self):
        result = NSSF(self.base).get_value()
        self.assertTrue(result)
        self.assertEqual(result,-3000)

    def testPAYE(self):
        result = PAYE(self.base,{}).get_value()
        self.assertTrue(result)
        self.assertEqual(result,500)

        result = PAYE(60000,{}).get_value()
        self.assertEqual(result,18000)

        result = PAYE(20000,{}).get_value()
        self.assertEqual(result,3540.4)
