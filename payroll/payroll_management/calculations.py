from abc import ABC,abstractmethod

upper_limit = 18000
lower_limit = 6000

class Calculation(ABC):
    """
        Abstract Base Class for all Calculations
    """

    def __init__(self,type):
        self.type = type

    @abstractmethod
    def get_value():
        pass

    @abstractmethod
    def perform_calculation():
        pass


class Deduction(Calculation):
    """
        Parent class for all deductions.Returns a negative value
    """

    def __init__(self,base):

        self.base_salary = base
        self.value = self.perform_calculation()
        super().__init__("Deduction")

    def get_value(self):
    	return -self.value

    def perform_calculation(self):
    	return 0


class Allowance(Calculation):
    """
        Parent class for all allownaces.Returns a positive value
    """

    def __init__(self):
        super().__init__("Deduction")

class Taxation(Calculation):
    """
        Parent class for all taxations.
    """

    def __init__(self,base):
        self.base_salary = base
        self.value = self.perform_calculation()
        super().__init__("Taxation")

    def get_value(self):
        return self.value

    def perform_calculation(self):
    	return 0


class NHIF(Deduction):

    def __init__(self,base):
        self.name = "NHIF"
        super().__init__(base)

    def perform_calculation(self,new_rates=None):
    	"""change error"""
    	rates = {
            range(0,6000):150,
            range(6000,8000):300,
            range(8000,12000):400,
            range(12000,15000):600,
            range(20000,25000):750,
            range(25000,30000):850,
            range(30000,35000):900,
            range(35000,40000):950,
            range(40000,45000):1000,
            range(45000,50000):1100,
            range(50000,60000):1200,
            range(60000,7000):1300,
            range(70000,80000):1400,
            range(80000,90000):1500,
            range(90000,100000):1600,
            range(100000,100000000000000):1700
        }

    	for key,value in rates.items():
            if self.base_salary in key:return value

class NSSF(Deduction):

    def __init__(self,base,lul=None,uul=None):
        self.name = "NSSF"
        self.upper_limit = upper_limit
        self.lower_limit = lower_limit

        if lul and uul != None:
            self.upper_limit = uul
            self.lower_limit = lul

        super().__init__(base)

    def perform_calculation(self):

    	rates = {
            range(0,self.lower_limit + 1): (0.06*self.base_salary),
            range(self.lower_limit + 1,self.upper_limit + 1): (0.06*self.lower_limit) + 0.06*(self.base_salary-self.lower_limit),
            range(self.upper_limit + 1,100000000000): (0.06*self.lower_limit) + (0.06*(self.upper_limit-self.lower_limit))
        }

    	for key,value in rates.items():
            if self.base_salary in key:return value

class CustomDeduction(Deduction):
    def __init__(self):
        pass

class Travel(Allowance):
    def __init__(self):
        pass

class Meal(Allowance):
    def __init__(self):
        pass

class CustomAllowance(Allowance):
    def __init__(self):
        pass

class PAYE(Taxation):
    """
        Calculates PAYE given the base salary
    """

    def __init__(self,base,allowances,admissible_deductions):
        self.name = "PAYE"
        self.allowances = allowances
        self.admissible_deductions = admissible_deductions
        self.base = base
        #self.relief = 1080

        super().__init__(self.base)


    @property
    def relief(self):
        return 1408

    """
    @__relief.setter
    def __relief(self,value):
        self.__relief = value"""

    def get_taxable(self):
        return self.base + sum(list(self.allowances.values())) + sum(list(self.admissible_deductions.values()))

    def perform_calculation(self):

        self.taxable_pay = self.get_taxable() #change to local,nonlocal
        self.taxable_pay_set = (0,)
        self.iteration_val , self.lower_limit, self.upper_limit = 11857,12298,47059

        def update_taxable(value,iteration=None):
            self.taxable_pay_set = self.taxable_pay_set.__add__((value,))
            self.taxable_pay -= iteration

        def update_taxable_in_range(percentage): #More testing
                if self.taxable_pay in range(0,self.iteration_val + 1) or self.taxable_pay > self.iteration_val:
                    update_taxable(self.taxable_pay*percentage,self.iteration_val)

        if self.taxable_pay <= self.lower_limit:
            value = self.taxable_pay * 0.1
            self.taxable_pay_set = self.taxable_pay_set.__add__((value,))

        elif self.lower_limit < self.taxable_pay < self.upper_limit:
            update_taxable(self.taxable_pay*0.1,self.lower_limit)

            update_taxable_in_range(0.2)

            update_taxable_in_range(0.25)

            update_taxable_in_range(0.3)
        else :
            value = self.taxable_pay * 0.3
            self.taxable_pay_set = self.taxable_pay_set.__add__((value,))

        return -sum(self.taxable_pay_set)


class PaySlipCalculator:

    def __init__(self,base_salary,allowances={},deductions={},admissible={}):
        self.base = base_salary
        self.allowances = {key:float(item) for key,item in allowances.items()}
        self.deductions = {key:float(item) for key,item in deductions.items()}
        self.custom_admissible = {key:float(item) for key,item in admissible.items()}
        self.paye = PAYE(self.base,self.allowances,self.get_admissible_deductions())

    def getNSSF(self):
        return float(NSSF(self.base).get_value())

    def getNHIF(self):
        return float(NHIF(self.base).get_value())

    def getPAYE(self):
        admissible_deductions = self.get_admissible_deductions()
        return float(self.paye.get_value()),(float(self.paye.get_value())+self.get_relief())

    def get_relief(self):
        return float(self.paye.relief)

    def get_taxable(self):
        return float(self.paye.get_taxable())

    def get_gross(self):
        return float(self.base + sum(self.get_allowances().values()))

    def get_admissible_deductions(self):
        result  =  {"NSSF":self.getNSSF()}
        result.update(self.custom_admissible)
        return result

    def get_deductions(self):
        result = {"NHIF":self.getNHIF()}
        result.update(self.deductions)
        return result

    def get_taxation(self):
        return {"PAYE":self.getPAYE()[0],"TAXABLE":self.get_taxable()}

    def get_allowances(self):
        return self.allowances

    def get_net_salary(self):
        return float((self.get_gross() + sum(self.get_admissible_deductions().values())) + ((self.getPAYE()[1]) + sum(self.get_deductions().values())))
