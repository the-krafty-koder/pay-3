from django.db import models
from employee_management.models import Firm
from django.contrib.auth.models import BaseUserManager,AbstractBaseUser,User

# Create your models here.
class UsersManager(BaseUserManager):
    def create_user(self,name,email,institution_name,password,employee=False):

        if not Firm.objects.get(firm_name=institution_name) :
            raise ValueError( "Firm must be present before attempting to log in")

        user = self.model(
            name = name,
            email = self.normalize_email(email),
            firm_name= institution_name,
            is_admin= not employee
        )

        user.set_password(password)
        user.save(using = self._db)
        return user

    def create_employee(self,name,email,institution_name,password):

        new_employee = self.create_user(name,email,institution_name,password,employee=True)
        return new_employee

    def create_super(self,name,email,password):
        user = self.model(
            name = name,
            email = self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using = self._db)
        return user


    def create_superuser(self,name,email,password):
        user = self.create_super(
            name = name,
            email = email,
        )
        user.set_password(password)
        is_admin = True
        user.save(using=self._db)
        return user


class Users(AbstractBaseUser):
    name = models.CharField(max_length=20, unique=True)
    email = models.EmailField()
    firm_name = models.CharField(max_length=50)


    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=True)

    objects = UsersManager()
    USERNAME_FIELD = 'name'
    REQUIRED_FIELDS = ['institution_name']

    def __str__(self):
        return  self.name

    @property
    def is_staff(self):
        return self.is_admin

class UserEmployee(Users):
    pass
