from django.db.models.signals import post_save
from django.dispatch import receiver

from employee_management.models import Employee

from .models import UserEmployee
from .passcode_generator import GeneratePassCode
from .tasks import send_login_credentials


@receiver(post_save, sender=Employee)
def create_employee_user(sender,instance,**kwargs):

    if kwargs.get("created")==True:
        employee_id = len(Employee.objects.all())
        password = GeneratePassCode(instance.firm.firm_name,employee_id).get_code()

        UserEmployee.objects.create_employee(
            instance.full_name,
            instance.email,
            instance.firm.firm_name,
            password
        )

        send_login_credentials(instance,password)

