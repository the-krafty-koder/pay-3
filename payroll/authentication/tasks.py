import logging
from celery.decorators import task
from .mail import send_login_mail

log = logging.getLogger(__name__)


@task(name="send_login_creds")
def send_login_credentials(employee, password):
    response = send_login_mail(employee.full_name, employee.email,
                               employee.firm.firm_name, password)
    if isinstance(response, True):
        return
    log.error(response)
