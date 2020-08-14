import logging
from .models import UserEmployee


class AuthBackend(object):
    def authenticate(self, name, institution_name, password):
        try:
            user = Users.objects.get(name=name,firm_name=institution_name,password=password)
            if user.check_password(password):
                return user
            else:
                return "Incorrect password"

        except Users.DoesNotExist:
            return logging.getLogger("error_logger").error("user with login %s does not exists " % login)

        except Exception as e:
            logging.getLogger("error_logger").error(repr(e))
            return None

    def authenticate_employee(self, name, institution_name, password):
        try:
            user = UserEmployee.objects.get(name=name, firm_name=institution_name,
                                            password=password)
            if user.check_password(password):
                return user
            else:
                return "Incorrect password"

        except UserEmployee.DoesNotExist:
            msg = "user with login %s does not exists "
            return logging.getLogger("error_logger").error(msg % login)

        except Exception as e:
            logging.getLogger("error_logger").error(repr(e))
            return None

    def get_user(self, name):
        try:
            user = Users.objects.get(name=name)
            if user.is_active:
                return user
            else:
                return None
        except Users.DoesNotExist:
            logging.getLogger("error_logger").error("user with username %s does not exist" % name)
