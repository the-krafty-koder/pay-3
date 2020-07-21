from django import template
from employee_management.models import FirmProfile

register = template.Library()

@register.filter(name='obj_type')
def field_type(object):
    return None if isinstance(object,list) else "dict"

@register.filter(name='filename')
def get_file_name(object):
    return object.name.split("/")[-1]

@register.filter(name='company_name')
def get_company_name(object):
    return "Mater Company"

@register.filter(name='company_logo')
def get_logo_url(object):
	""" Gets firm_name from logged in user and obtains firm logo"""

	return FirmProfile.objects.get(firm_name="Mater Compan").logo.url
