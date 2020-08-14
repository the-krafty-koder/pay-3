import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

SENDGRID_API_KEY = os.environ.get('SENDGRID_API_KEY')


def send_login_mail(name, email, firm_name, password):
    message = Mail(
        from_email='feradwight@gmail.com',
        to_emails=f'{email}' ,
        subject='Login Credentials')

    message.template_id = 'd-faf9f4d3a666491c9cf0f24027322525'
    message.dynamic_template_data = {
        "employee_name": name,
        "firm_name": firm_name,
        "employee_password": password
    }

    try:
        sg = SendGridAPIClient()
        response = sg.send(message)
        return response.status_code == 202
    except Exception as e:
        return e.message
