from django.db import models
from django.core.validators import (RegexValidator,
                                    EmailValidator)

from picklefield.fields import PickledObjectField

# Create your models here.

class FirmManager(models.Manager):

    def get_all_employees(self):
        return Employees.objects.filter(firm=self.model)

    def get_number_employees(self):
        return Employees.objects.filter(firm=self.model).__len__()


def logo_file_path(instance, filename):
    return "uploads/institution_{0}/images/logo".format(instance.firm_name)


class FirmProfile(models.Model):
    firm_name = models.CharField(max_length=50)
    logo = models.ImageField(upload_to=logo_file_path, null=True)
    website = models.URLField()
    mailing_address = models.TextField()

    def __str__(self):
        return self.firm_name


class Firm(models.Model):
    firm_name = models.CharField(max_length=30, primary_key=True)
    email = models.EmailField(null=True)
    address = models.TextField(max_length=30)
    firm_profile = models.ForeignKey(
        FirmProfile,
        on_delete=models.CASCADE,
        related_name="firm_profile",
        null=True
    )
    objects = FirmManager()

    def __str__(self):
        return self.firm_name

    def get_all_employees(self):
        return Employee.objects.filter(firm=self)

    def get_number_employees(self):
        return Employee.objects.filter(firm=self).__len__()


class Contract(models.Model):
    employee_name = models.CharField(max_length=50, default="None")
    start_date = models.DateField(auto_now=False, auto_now_add=False, null=True)
    end_date = models.DateField(auto_now=False, auto_now_add=False, null=True)
    contract_type = models.CharField(max_length=15)
    base_salary = models.FloatField()
    allowances = PickledObjectField(null=True, default=dict)

    def __str__(self):
       return "Employee Contract:{}".format(self.employee_name)



def image_file_path(instance,filename):
        return "uploads/institution_{0}/employee/employee_{1}/images/{2}".format("Jos Org",instance.full_name,filename)##edit!!


class Employee(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    full_name = models.CharField(max_length=50,primary_key=True)
    home_address = models.TextField(max_length=50)
    phone_regex  = RegexValidator(regex=r'^\+?1?\d{9,13}$',
                                  message="Phone number must be in the format +11111111111")
    phone_number = models.CharField(max_length=13,unique=True)
    email_validator = EmailValidator(message="Enter a valid email address")
    email = models.EmailField(max_length=254)
    gender = models.CharField(max_length=5,default=None,null=True)

    image = models.ImageField(null=True, default=None, upload_to=image_file_path)

    kra_pin = models.TextField(max_length=30,unique=True)
    nhif_number = models.TextField(unique=True)
    nssf_number = models.TextField(unique=True)
    contract = models.OneToOneField(
        Contract,
        on_delete = models.CASCADE,
        related_name = "employee_contract",
        null=True
    )
    identification_number=models.CharField(max_length=40,default=None,null=True)

    department = models.CharField(max_length=20)
    is_manager = models.BooleanField()
    firm = models.ForeignKey(
        Firm,
        on_delete=models.CASCADE,
        related_name="firm",
        null=True
    )
    education = PickledObjectField(null=True,default=list)
    documents = PickledObjectField(null=True,default=list)


    def __str__(self):
        return "{} {}".format(self.first_name,self.last_name)

    def save(self,*args,**kwargs):
        self.full_name = self.__str__()
        super(Employee,self).save(*args,**kwargs)


def education_file_path(instance,filename):
    msg = "uploads/institution_{0}/employee/employee_{1}/education/{2}"
    return msg.format("Jos Org", instance.employee, filename)  # edit!!


class Education(models.Model):
    employee = models.CharField(max_length=20)
    level = models.CharField(max_length=20)
    start_year = models.CharField(max_length=4)
    end_year = models.CharField(max_length=4)

    files = models.FileField(upload_to=education_file_path)


def document_file_path(instance, filename):
    path = "uploads/institution_{0}/employee/employee_{1}/documents/{2}"
    return path.format("Jos Org", instance.employee, filename)  # edit!!


class Document(models.Model):
    employee = models.CharField(max_length=20)
    name = models.CharField(max_length=20)
    files = models.FileField(upload_to=document_file_path)


def temp_file_path(instance, filename):
    path = "uploads/institution_{0}/employee/employee_{1}/images/{2}"
    return path.format("Jos Org", instance.employee, filename)  # edit!!


class UploadedImage(models.Model):
    employee = models.CharField(max_length=50)
    image = models.ImageField(upload_to=temp_file_path)
