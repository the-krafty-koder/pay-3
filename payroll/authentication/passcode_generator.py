from django.core.signing import TimestampSigner


class GeneratePassCode:

    def __init__(self,firm_name,employee_id):
        self.firm_name = firm_name
        self.employee_id = employee_id

    def get_string(self,id_string):
        signer = TimestampSigner(salt="extra")
        value = signer.sign(id_string)

        return value

    def get_code(self):
        code = self.get_string(f'{self.firm_name}:{self.employee_id}')
        return code
